# ReelChain v3.5 -- Chain Building Interaction Brief

**Priority:** P1 (immediately after current P0 stabilisation)

## Purpose

The gameplay is now working well enough that interaction quality has
become the next priority.

This iteration is **not** about adding features.

It is about making every move feel satisfying and making the player feel
like they are physically constructing a Reel Chain.

The player should never feel like they are navigating software.

They should feel like they are building something.

------------------------------------------------------------------------

# Creative Direction (Important)

The accompanying HTML mock-up and **Concept A -- The Puzzle** image are
**creative direction**, **not pixel-perfect specifications**.

Their purpose is to communicate the feeling we are aiming for.

They should **not** be recreated literally.

The implementation should preserve the philosophy while improving on the
design where appropriate.

### The philosophy

-   The puzzle is the hero.
-   The first thing the player sees is the two movie posters.
-   Almost no dashboard UI.
-   The objective is understood in under a second.
-   The player immediately wants to touch the screen.
-   The interaction should feel calm, tactile and rewarding.

If the implementation can improve on the mock-up while preserving this
philosophy, **improve it**.

------------------------------------------------------------------------

# Interaction Philosophy

Borrow more from Apple interaction design, Nintendo, Monument Valley and
Duolingo than from forms, menus, database interfaces or IMDb.

The interaction should feel continuous, tactile and playful.

------------------------------------------------------------------------

# Core Principle

> **The chain is always visible.**

The player never leaves the chain.

Every interaction extends it.

No navigation between gameplay screens.

------------------------------------------------------------------------

# New Interaction

1.  Show the start movie, target movie and available actors.
2.  Player taps an actor.
3.  The actor animates into the chain.
4.  The rest of the UI subtly de-emphasises.
5.  Display "Bradley Cooper starred in...".
6.  Animate 4--6 movie posters upwards like cards being dealt.
7.  If more movies exist, show **+X more**.
8.  Player taps a poster.
9.  The poster animates into the chain.
10. The next actors appear beneath.
11. Repeat.

------------------------------------------------------------------------

# Motion Principles

Movie → Actor → Movie → Actor → Movie

Nothing should simply replace something else.

Everything should move into position.

The chain should literally construct itself.

Avoid hard cuts, page navigation, modal windows and long fades.

Prefer lift, slide, snap, expand and settle animations with subtle
momentum.

------------------------------------------------------------------------

# Visual Principles

## Movie selection

-   Poster first.
-   Title second.
-   Avoid text-heavy interfaces.

## Actor selection

-   Large headshots.
-   Small names.
-   No long lists or dropdowns.

------------------------------------------------------------------------

# Success Criteria

-   The chain is always visible.
-   Every tap visibly extends the chain.
-   The player never feels like they left the puzzle.
-   Movie recognition is immediate.
-   The interaction encourages **One more go**.

------------------------------------------------------------------------

# Guiding Principle

> **Every tap should create a small dopamine hit.**

If a player smiles after placing another movie into the chain, we've
succeeded.
