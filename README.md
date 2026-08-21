# LLMs grading LLMs—with receipts

**Track:** Module 5 — Evaluation & strategy · **When:** Week 7, Day 4 · **Status:** Required

This repository contains everything you need for this lab.

## Files

- [`instructions.md`](./instructions.md) — the lab instructions
- [`rubric.md`](./rubric.md) — how your submission is graded; this is what the AI reviewer checks your PR against

## How to complete this lab

1. **Fork** this repository.
2. Do the work described in `instructions.md`, committing to your fork.
3. Open a **pull request** back into this repository.
4. You'll receive **AI feedback** on your PR based on `rubric.md`. Address any blocking feedback and push updates to the same PR.

## Submission hygiene

- Keep this repository scoped to this lab only — no unrelated projects or personal files.
- Use clear, descriptive filenames.
- Remove secrets, API keys, and tokens before committing.

## Scenario

Nordbank, a mid-sized German retail bank, wants to use an LLM to draft the letters sent to applicants whose consumer loan application has been declined. A human loan officer reviews and signs each letter, but the model produces the full first draft from a structured decision record (applicant name, product, decision date, primary and secondary decline reasons, credit bureau reference).

Each letter must state the actual decline reason from the decision record and no other reason, tell the applicant they can request a manual review and how, reference the credit bureau consulted where a bureau score contributed to the decision, stay under 300 words, and read as plain, non-condescending German business prose.

The main concerns, in order of how much they would hurt the client, are: the model inventing or softening the decline reason, which is both a hallucination and a compliance breach; the letter omitting the manual review right or the bureau reference, which is a silent regulatory failure that no one notices until an audit; and tone drift, either cold and boilerplate or falsely warm and apologetic in a way that implies the decision might be reversed.
