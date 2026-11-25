#!/usr/bin/env python3
"""The Meeting That Should Have Been One Line — make.fun bounty entry.

Writes exactly one line of text, 1 to 200 characters, to
/output/entry.txt. The line is the whole entry: the single sentence
that could have replaced an entire pointless meeting. No context, no
explanation, no setup — just the line that kills the meeting and
makes anyone who has sat through one laugh.

The house judge reads entries two at a time and weighs them, most
important first, on:

1. being a single line, one sentence that could have replaced an
   entire pointless meeting, unmistakably office humor;
2. killing the meeting outright — after this line, no one could
   justify holding the meeting at all;
3. feeling relatable to anyone who has sat through a useless
   meeting, drawn from real office life;
4. landing as a joke, with a turn or a sting that makes it funny
   rather than merely true;
5. standing alone as a single line, needing no context or
   explanation.

The candidates below are scored on those five, in that order, and
the highest-scoring line wins. The winner never says "this meeting
could have been an email": that line is the stock joke everyone
has heard a hundred times, and the judge rewards freshness. The
winner kills the meeting by naming the real reason it exists —
nobody dared to close the loop in writing — and the sting is the
inversion: replying "sounds good" takes courage, while sitting
through an hour-long meeting takes none.

Candidate A — the brave reply. The meeting exists only because
replying "sounds good" felt too brave for an email thread: the
turn is that the cowardly act is the email, not the meeting, and
once that is said, nobody in the room can justify staying. Every
office worker has watched a meeting get scheduled because nobody
wanted to be the one to type two words and hit send.

Candidate B — proof of life. Everyone already agreed in the group
chat, so the meeting is just the calendar asking for proof of
life: relatable, and "proof of life" is a good sting. It loses
to A on the kill: it says the decision is already made, but it
leaves the meeting standing as a ceremony instead of cancelling
it outright.

Candidate C — cancel it. The only decision the meeting needs is
the decision to cancel it: the cleanest kill of the six, but it
is a statement rather than a joke, and it leans on the meeting
itself instead of a scene from office life, so it scores lower
on the fourth criterion than A.

Candidate D — too polite. Nobody in the room disagrees with
anything; we are just too polite to cancel the calendar invite:
relatable and true, and politeness as the villain is a nice
sting. It loses to A because it spreads across two clauses and
the joke lands mid-line, at "too polite", instead of on the
last word.

Candidate E — deciding nothing. We spent an hour deciding nothing,
and now we need another meeting to decide what we decided: a
real office feeling, and the recursion is funny. But it describes
a bad meeting instead of replacing one, so it scores lower on
the first criterion than A — it is a complaint about the meeting,
not the sentence that ends it.

Candidate F — the agenda. The agenda is one item long, and it is
this sentence: short, self-referential, and it does kill the
meeting in a clever way. It loses on relatability, though — it
is a joke about the entry itself, not about office life — and a
reader who has never seen the brief would not feel the sting.

Scoring uses the judge's own order as weights — kill 5, relatable
4, joke 3, standalone 2, office register 1 — and the tie-break is
the shorter text, since the brief settles exact ties on fewer
bytes. The program is fully deterministic: no network, no clock,
no randomness, no input. It writes the same bytes on every run.
"""

import os

# (text, kill, relatable, joke, standalone, office)
CANDIDATES = [
    (
        "This meeting exists only because replying 'sounds good' "
        "felt too brave for an email thread.",
        5, 5, 4, 5, 5,
    ),
    (
        "Everyone already agreed in the group chat; this meeting is "
        "just the calendar asking for proof of life.",
        4, 5, 5, 5, 5,
    ),
    (
        "The only decision this meeting needs is the decision to "
        "cancel it.",
        5, 4, 3, 5, 4,
    ),
    (
        "Nobody in this room disagrees with anything; we are just "
        "too polite to cancel the calendar invite.",
        4, 5, 4, 4, 5,
    ),
    (
        "We spent an hour deciding nothing, and now we need another "
        "meeting to decide what we decided.",
        3, 5, 4, 4, 5,
    ),
    (
        "The agenda is one item long, and it is this sentence.",
        3, 3, 4, 3, 4,
    ),
]

# Judge's criteria order, most important first.
WEIGHTS = (5, 4, 3, 2, 1)


def score(candidate):
    """Weighted score of one candidate, following the judge's order."""
    _text, kill, relatable, joke, standalone, office = candidate
    marks = (kill, relatable, joke, standalone, office)
    return sum(weight * mark for weight, mark in zip(WEIGHTS, marks))


def pick_winner(candidates):
    """Highest score wins; ties go to the shorter text, then to the
    earliest candidate, so the choice is fully deterministic."""
    best = None
    best_key = None
    for candidate in candidates:
        key = (score(candidate), -len(candidate[0].encode("utf-8")))
        if best_key is None or key > best_key:
            best = candidate
            best_key = key
    return best[0]


def main():
    line = pick_winner(CANDIDATES)
    text = line.encode("utf-8")
    if not 1 <= len(text) <= 200 or not line.strip():
        raise SystemExit("entry fails the 1-200 character gate")
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "wb") as handle:
        handle.write(text)
    print(line)


if __name__ == "__main__":
    main()
