ReelChain v3 – Gameplay & Scoring Redesign

We've spent some time stepping back from the implementation and thinking about what makes ReelChain enjoyable. The conclusion is that the scoring system and gameplay model should be simplified together.

The current version contains too many overlapping systems (rounds, runs, Hall of Fame, time, reveals, hints, steps, perfect multipliers etc.) and the player doesn't really understand what they're being rewarded for.

This redesign establishes a much clearer game loop.

1. The Core Gameplay Loop

The game is no longer about trying to achieve a perfect score.

The game is about building the longest Run possible.

The gameplay loop becomes:

Start Run
      ↓
Solve a chain
      ↓
Earn Fame
      ↓
Continue Run?
      ↓
Yes → next chain
      ↓
Reach Run milestones (3 / 6 / 9)
      ↓
Earn Run bonuses
      ↓
Continue...

OR

Give Up
      ↓
Run ends
      ↓
Reveal optimal chain
      ↓
Start new Run

This creates a much more compelling "one more round" loop.

2. There is no "Lose"

This was the biggest design decision.

Do not introduce:

move limits
life systems
timers
forced failure

Instead the player always has a choice.

They either:

keep trying

or

Give Up.

Giving Up ends the Run.

That creates tension without frustration.

The player feels responsible for ending their Run rather than the game punishing them.

3. Reveal should disappear

The current Reveal button doesn't fit this model.

Reveal is effectively admitting:

"I can't solve this."

Therefore Reveal should simply become the consequence of Give Up.

New flow:

Player presses

Give Up

Confirmation:

Give up?

Your current Run will end.

We'll show you the shortest chain before starting another.

Buttons

Keep Looking

Give Up

After Give Up:

Run ends
Show optimal chain
Start another Run

No separate Reveal button required.

4. Simplify the scoring philosophy

Players should understand scoring instantly.

Score should answer one question:

How well did I solve THIS chain?

Nothing else.

Hall of Fame

Run

Progression

should not influence this calculation.

Suggested scoring inputs:

Difficulty

Easy
Medium
Hard

Chain efficiency

Optimal chain?
Extra links?

Exploration

Wrong turns
Backtracks

Help

Hints
Second Take

That's it.

No time scoring.

5. Perfect Chain

Perfect should become rare and obvious.

A Perfect Chain means:

optimal chain
no backtracking
no hints
no Second Take

Time does not matter.

Players should never lose Perfect because they stopped to think.

6. Fame

Fame represents career progression.

It is earned every completed chain.

Example only:

Easy 30

Medium 40

Hard 50

Then subtract for:

extra links

backtracking

hints

Second Take

Minimum completion reward still applies.

7. Hall of Fame

Hall of Fame should NOT modify scoring.

Its purpose is different.

Hall of Fame should simply unlock progressively harder puzzles.

As players improve they naturally encounter more difficult chains worth more Fame.

No hidden score multipliers.

No Hall-of-Fame bonus.

Think of it as matchmaking rather than scoring.

8. Runs

Runs are now the central retention mechanic.

Every completed chain extends the Run.

Giving Up ends the Run.

Run milestones:

3 completed chains

6 completed chains

9 completed chains

Each milestone awards a Fame bonus.

This bonus should appear separately from the round score.

Example:

Round Fame          +38

🔥 Run Bonus         +5

Total Earned        43 Fame

The Run bonus rewards consistency.

The Round score rewards skill.

These should never be mixed together.

9. UI simplification

The home screen currently contains too many competing concepts.

Current:

Round

Run Streak

Fame

Status

Hall of Fame

Timer

Challenge

Avatar

Hint

End

etc.

The player doesn't know what matters.

Instead I'd simplify the hierarchy.

Primary

🔥 Current Run

⭐ Fame

🏆 Hall of Fame

Everything else is secondary.

10. Gameplay screen

Current buttons:

Back

Reveal

Flip

Recommended:

Back

Hint

Give Up

Flip

Reveal disappears.

Give Up becomes the single exit from a puzzle.

11. Timer

Remove it from prominence.

It isn't part of scoring.

It isn't part of gameplay.

It creates pressure without purpose.

If retained at all it should be tiny and informational only.

12. End-of-round screen

The player should understand exactly why they earned their Fame.

Example

Complete Chain

Difficulty (Medium)        +40
Extra links                 -5
Backtracking                -2
Hints                        0

Round Fame                 33

🔥 Run Bonus               +5

Total Earned              38 Fame

Run continues... "One more round"

or

You Gave Up

Run ended at 6 chains.

Here's the shortest chain.

[Start New Run]
Design philosophy

The previous system attempted to reward everything simultaneously.

The new system gives each mechanic a single responsibility:

Round Score → How well did I solve this chain?
Run → How long can I keep going?
Fame → My accumulated career progress.
Hall of Fame → Which level of challenges should I now receive?

When each system answers only one question, the game becomes much easier to understand, easier to balance, and much more addictive.