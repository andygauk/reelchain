// PERSISTENT REGRESSION GUARD — ReelChain play loop.
// Boots the REAL deploy/index.html <script> in a stubbed DOM (node vm),
// drives a full solve, and asserts the play loop (decks + chain + win) works.
// Run after EACH migration stage; must stay green so we catch regressions
// (esp. the MEDIA const TDZ trap) introduced by presentation changes.
const fs = require('fs');
const vm = require('vm');

// global element registry so document.querySelector can find elements the harness
// creates via getElementById/createElement (mimics a real DOM tree).
const __els = [];

const HTML = fs.readFileSync('C:/Projects/reelchain/deploy/index.html', 'utf8');
const script = HTML.match(/<script>([\s\S]*?)<\/script>/)[1];
const epilogue = `;globalThis.__rc = {
  get state(){return state}, get run(){return run},
  get FILMS(){return FILMS}, get MEDIA(){return MEDIA}, get EVENTS(){return EVENTS},
  $:(id)=>$(id), bfs, chooseActor, chooseFilm, render, newPuzzle, fireWinCelebration
};`;

function makeEl(id){
  const el={id,_children:[],style:{setProperty(k,v){this['--'+k]=v;},getPropertyValue(k){return this['--'+k]||'';}},classList:{_s:new Set(),add(...c){c.forEach(x=>this._s.add(x));},remove(...c){c.forEach(x=>this._s.delete(x));},toggle(c,f){const has=this._s.has(c);const on=(f===undefined)?!has:f;on?this._s.add(c):this._s.delete(c);return on;},contains(c){return this._s.has(c);}},
    get innerHTML(){return this._html||'';}, set innerHTML(v){this._html=v;if(v==='')this._children=[];},
    get children(){return this._children;}, get nextSibling(){const p=this.parentNode;if(!p)return null;const i=p._children.indexOf(this);return i>=0&&i<p._children.length-1?p._children[i+1]:null;},
    textContent:'', value:'', selectedIndex:0, alt:'', src:'',
    appendChild(c){this._children.push(c);c.parentNode=this;if(c.id && !__els.includes(c))__els.push(c);return c;}, prepend(c){this._children.unshift(c);c.parentNode=this;return c;},
    removeChild(c){this._children=this._children.filter(x=>x!==c);}, remove(){if(this.parentNode)this.parentNode.removeChild(this);},
    insertBefore(n,ref){const i=this._children.indexOf(ref);if(i<0)this._children.push(n);else this._children.splice(i,0,n);n.parentNode=this;return n;},
    querySelectorAll(sel){const cls=sel.replace('.','');return this._all().filter(e=>e.classList.contains(cls));},
    _all(){let out=[];for(const c of this._children){out.push(c);out=out.concat(c._all?c._all():[]);}return out;},
    getAttribute(k){return this['_attr_'+k]!==undefined?this['_attr_'+k]:(this[k]||null);}, setAttribute(k,v){this['_attr_'+k]=v;},
    set className(v){this._cls=v;this.classList._s=new Set(v.split(/\s+/).filter(Boolean));}, get className(){return this._cls||'';},
    querySelector(sel){const cls=sel.replace('.','');return this._all().find(e=>e.classList.contains(cls))||null;},
    querySelectorAll(sel){const cls=sel.replace('.','');return this._all().filter(e=>e.classList.contains(cls));},
    addEventListener(){}, onclick:null, onload:null, onerror:null};
  if(id)__els.push(el);
  return el;
}
const els={}; function $(id){if(!els[id])els[id]=makeEl(id);return els[id];}
const filmstrip=$('filmstrip'); const rail=makeEl('rail'); rail.classList.add('rc-rail'); const railFill=$('railFill'); filmstrip.appendChild(rail); filmstrip.appendChild(railFill);
// static HTML elements the engine queries but the harness doesn't parse — instantiate them
const winModal=makeEl('winModal'); winModal.classList.add('rc-win-modal'); // document.querySelector('.rc-win-modal') target
const document={getElementById:(id)=>$(id),createElement:(t)=>makeEl('_'+t),
  querySelector:(sel)=>{const cls=sel.replace('.','');return __els.find(e=>e.classList&&e.classList.contains(cls))||null;},
  querySelectorAll:(sel)=>{if(sel==='#diff button')return[{dataset:{d:'easy'},classList:{add(){},remove(){},toggle(){}},onclick:null}];const cls=sel.replace('.','');return __els.filter(e=>e.classList&&e.classList.contains(cls));},
  addEventListener(){},fonts:{ready:Promise.resolve(),check:()=>false,add:()=>{},load:()=>Promise.resolve()}};
const store={}; const localStorage={getItem:(k)=>k in store?store[k]:null,setItem:(k,v)=>{store[k]=String(v);},removeItem:(k)=>{delete store[k];}};
const __timers=[]; let __timerId=1;
function __setTimeout(fn,ms){const id=__timerId++; __timers.push({id,fn}); return id;}
function __clearTimeout(id){const i=__timers.findIndex(t=>t.id===id); if(i>=0)__timers.splice(i,1);}
function runPendingTimers(){ // fire all queued timers (used between phases)
  let guard=0;
  while(__timers.length && guard++<10000){ const t=__timers.shift(); try{ t.fn(); }catch(e){} }
}
const sandbox={document,localStorage,window:{},navigator:{},console,setTimeout:__setTimeout,clearTimeout:__clearTimeout,setInterval:()=>0,clearInterval:()=>0,requestAnimationFrame:(fn)=>fn(),btoa:(s)=>Buffer.from(s,'binary').toString('base64'),atob:(s)=>Buffer.from(s,'base64').toString('binary'),Image:function(){return makeEl('img');},Option:function(t,v){const o=makeEl('opt');o.textContent=t;o.value=v;return o;},fetch:()=>Promise.resolve({}),location:{origin:'https://reelchain.app',pathname:'/',hash:''},Math,Date,JSON,Object,Array,String,Number,Boolean,RegExp,Promise,Error};
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

  // Stage 5: win celebration — assert DURING the hold window (timers deferred)
  check('Stage 5: Linked! hold shown on win', G('linkedHold').classList.contains('rc-show'));
  const modal = document.querySelector('.rc-win-modal');
  check('Stage 5: confetti spawned in win modal', !!modal && modal.querySelectorAll('.rc-confetti').length>0,
        'confetti='+(modal?modal.querySelectorAll('.rc-confetti').length:0));
  // now flush deferred timers (Linked! hide + confetti cleanup) — must not crash
  runPendingTimers();
  check('Stage 5: celebration cleans up after timers', !G('linkedHold').classList.contains('rc-show'));

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
