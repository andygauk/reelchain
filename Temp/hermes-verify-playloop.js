// PERSISTENT REGRESSION GUARD — ReelChain play loop.
// Boots the REAL deploy/index.html <script> in a stubbed DOM (node vm),
// drives a full solve, and asserts the play loop (decks + chain + win) works.
// Run after EACH migration stage; must stay green so we catch regressions
// (esp. the MEDIA const TDZ trap) introduced by presentation changes.
const fs = require('fs');
const vm = require('vm');

const HTML = fs.readFileSync('C:/Projects/reelchain/deploy/index.html', 'utf8');
const script = HTML.match(/<script>([\s\S]*?)<\/script>/)[1];
const epilogue = `;globalThis.__rc = {
  get state(){return state}, get run(){return run},
  get FILMS(){return FILMS}, get MEDIA(){return MEDIA}, get EVENTS(){return EVENTS},
  $:(id)=>$(id), bfs, chooseActor, chooseFilm, render, newPuzzle
};`;

function makeEl(id){
  const el={id,_children:[],style:{},classList:{_s:new Set(),add(...c){c.forEach(x=>this._s.add(x));},remove(...c){c.forEach(x=>this._s.delete(x));},toggle(c,f){const has=this._s.has(c);const on=(f===undefined)?!has:f;on?this._s.add(c):this._s.delete(c);return on;},contains(c){return this._s.has(c);}},
    get innerHTML(){return this._html||'';}, set innerHTML(v){this._html=v;if(v==='')this._children=[];},
    get children(){return this._children;}, get nextSibling(){const p=this.parentNode;if(!p)return null;const i=p._children.indexOf(this);return i>=0&&i<p._children.length-1?p._children[i+1]:null;},
    textContent:'', value:'', selectedIndex:0, alt:'', src:'',
    appendChild(c){this._children.push(c);c.parentNode=this;return c;}, prepend(c){this._children.unshift(c);c.parentNode=this;return c;},
    removeChild(c){this._children=this._children.filter(x=>x!==c);}, remove(){if(this.parentNode)this.parentNode.removeChild(this);},
    insertBefore(n,ref){const i=this._children.indexOf(ref);if(i<0)this._children.push(n);else this._children.splice(i,0,n);n.parentNode=this;return n;},
    querySelectorAll(sel){const cls=sel.replace('.','');return this._all().filter(e=>e.classList.contains(cls));},
    _all(){let out=[];for(const c of this._children){out.push(c);out=out.concat(c._all?c._all():[]);}return out;},
    getAttribute(k){return this['_attr_'+k]!==undefined?this['_attr_'+k]:(this[k]||null);}, setAttribute(k,v){this['_attr_'+k]=v;},
    set className(v){this._cls=v;this._s=new Set(v.split(/\s+/).filter(Boolean));}, get className(){return this._cls||'';},
    addEventListener(){}, onclick:null, onload:null, onerror:null};
  return el;
}
const els={}; function $(id){if(!els[id])els[id]=makeEl(id);return els[id];}
const filmstrip=$('filmstrip'); const rail=makeEl('rail'); rail.classList.add('rc-rail'); const railFill=$('railFill'); filmstrip.appendChild(rail); filmstrip.appendChild(railFill);
const document={getElementById:(id)=>$(id),createElement:(t)=>makeEl('_'+t),querySelectorAll:(sel)=>{if(sel==='#diff button')return[{dataset:{d:'easy'},classList:{add(){},remove(){},toggle(){}},onclick:null}];return [];},addEventListener(){}};
const store={}; const localStorage={getItem:(k)=>k in store?store[k]:null,setItem:(k,v)=>{store[k]=String(v);},removeItem:(k)=>{delete store[k];}};
const sandbox={document,localStorage,window:{},navigator:{},console,setTimeout:(fn)=>fn(),clearTimeout,setInterval:()=>0,clearInterval,requestAnimationFrame:(fn)=>fn(),btoa:(s)=>Buffer.from(s,'binary').toString('base64'),atob:(s)=>Buffer.from(s,'base64').toString('binary'),Image:function(){return makeEl('img');},Option:function(t,v){const o=makeEl('opt');o.textContent=t;o.value=v;return o;},fetch:()=>Promise.resolve({}),location:{origin:'https://reelchain.app',pathname:'/',hash:''},Math,Date,JSON,Object,Array,String,Number,Boolean,RegExp,Promise,Error};
sandbox.window=sandbox; sandbox.globalThis=sandbox; vm.createContext(sandbox);

let results=[]; function check(name,cond,extra){results.push({name,ok:!!cond,extra:extra||''});}
try{ vm.runInContext(script+epilogue,sandbox,{filename:'rc-inline.js'}); check('script boots (no MEDIA TDZ)',true); }
catch(e){ check('script boots (no MEDIA TDZ)',false,e.message); report(); process.exit(1); }

const R=sandbox.__rc;
function G(id){return R.$(id);}

try{
  // After boot, the actor deck (current film's cast) should be populated.
  const actorCount = G('actorDeck').children.length;
  check('actor deck populated on boot', actorCount>0, 'count='+actorCount);
  check('film deck hidden on boot', G('filmDeck').style.display==='none' || G('filmDeck').children.length===0);

  // Tap the first actor -> film deck should populate.
  const a0 = R.state.current;
  // pick an actor that actually advances (use bfs to choose a winning first actor)
  const b=R.bfs(a0, R.state.target);
  let firstActor=null, firstFilm=null, done=false;
  for(let i=0;i<b.chain.length&&!done;i++){ if(b.chain[i].type==='actor'){ firstActor=b.chain[i].name; R.chooseActor(firstActor); break; } }
  check('film deck populated after chooseActor', G('filmDeck').children.length>0, 'count='+G('filmDeck').children.length);

  // solve fully
  for(let i=0;i<b.chain.length&&!done;i++){
    if(b.chain[i].type==='actor'){ const actor=b.chain[i].name; R.chooseActor(actor); const nf=b.chain[i+1].name; R.chooseFilm(nf); if(nf===R.state.target)done=true; }
  }
  check('solve opens win overlay', G('overlay').classList.contains('rc-open'));
  check('win title is CHAIN COMPLETE', G('winTitle').textContent.indexOf('CHAIN COMPLETE')>=0, G('winTitle').textContent);
  check('Fame line shows +N Fame', /\+\d+ Fame/.test(G('winFame').textContent), G('winFame').textContent);

  // analytics taxonomy intact
  const evs=R.EVENTS.map(e=>e.event);
  check('game_completed fired', evs.includes('game_completed'));
  check('NO old round_completed', !evs.includes('round_completed'));
  // engine still preserves: scoring applied to run
  check('Run Fame increased after solve', R.run.fame>0, 'fame='+R.run.fame);

  // Challenge a friend still wired to share sheet
  check('Challenge a friend -> shareCard', G('winShare').onclick === sandbox.shareCard);
}catch(e){ check('play loop path', false, e.message); }

report();
function report(){let pass=0,fail=0;for(const r of results){console.log((r.ok?'PASS':'FAIL')+' '+r.name+(r.extra?('  ['+r.extra+']'):''));r.ok?pass++:fail++;}console.log('\nPLAY-LOOP REGRESSION: '+pass+' passed, '+fail+' failed');process.exit(fail?1:0);}
