# Thesis Project Team & Execution Strategy

As the **Accurate Lead Agent** for Hamid Asgharian's master's thesis, I am establishing this document to define the roles of our multi-agent team and outline exactly how we will proceed to guarantee an academically rigorous, ideal final output. 

The core philosophy of this project is **Accuracy and Rigor over Speed**.

## The Team

### 1. Lead Agent (Me)
*   **Role:** Project Manager, Content Strategist, and Final Decision Maker.
*   **Responsibilities:** 
    *   Make all judgment calls on thesis claims, framing, and structure.
    *   Direct the workflow and assign specific tasks to the other agents.
    *   Evaluate all evidence before approving a task as complete.
    *   Ensure any negative or unexpected simulation results are documented honestly as academic findings, rather than hidden.
*   **Rule:** I do not blindly trust the output of other agents; I verify.

### 2. OpenCode (Pure Operator)
*   **Role:** Execution Engine.
*   **Responsibilities:**
    *   Edit Python simulation code and run experiments locally.
    *   Apply exact text edits to the canonical `thesis_full.md` document *as instructed by the Lead*.
    *   Manage the `results/` directory (images, CSVs).
    *   Run the final DOCX generation pipeline (`pandoc`).
*   **Rule:** OpenCode must **never** claim a task is "done" without pasting direct evidence (e.g., terminal output, `grep` results, exact file contents). OpenCode does not make independent content or framing decisions.

### 3. QA Agent (Standards and Quality)
*   **Role:** Academic Standard Enforcer.
*   **Responsibilities:**
    *   Review the thesis against the university's template and formatting requirements.
    *   Ensure tone, flow, and grammatical quality meet master's level academic standards.
    *   Flag redundancies, structural issues, or inconsistencies.
*   **Rule:** QA suggests improvements and flags errors, but final content approval rests with the Lead. 

### 4. NotebookLM (Accurate Resources)
*   **Role:** Source of Truth for References.
*   **Responsibilities:**
    *   Hold the actual source PDFs of the bibliography.
    *   Perform literal extraction (pulling exact titles, authors, venues, and specific claims directly from the text of the source's first page or body).
*   **Rule:** NotebookLM is used for **literal extraction only**. We do not trust its summaries or judgment calls, as it has previously hallucinated or pulled from the wrong document. All extracted claims must explicitly specify "from the source file itself."

---

## How the Project Must Continue (Ideal Output Strategy)

To reach a flawless final submission, the team will execute the following phases in strict order. **No phase will begin until the previous one is fully verified.**

### Phase 1: Complete the Bibliography Audit
**Lead + NotebookLM**
*   *Action:* Resolve the critical missing citation (Alshehri & Gaunt, 2020) and audit the remaining ~14 unchecked references.
*   *Standard:* Every citation in Chapter 6 must correspond to a real, verifiable paper. If it is fabricated or irretrievable, it gets cut, and the text relying on it is rewritten.

### Phase 2: In-Text Claim Verification
**Lead + NotebookLM + QA**
*   *Action:* Sentence-by-sentence pass to ensure every claim citing a paper accurately reflects the source material. 
*   *Standard:* NotebookLM extracts the literal text from the PDF; the Lead evaluates if the thesis claim matches; OpenCode edits if a correction is needed.

### Phase 3: Structural and Template Compliance
**Lead + QA + OpenCode**
*   *Action:* Rename all chapters to match the exact university Persian template (کلیات / مبانی نظری و پیشینه تحقیق / روش پیشنهادی / تجزیه و تحلیل نتایج / نتیجه‌گیری).
*   *Standard:* QA verifies that all front-matter, headings, and appendix conventions perfectly match the university guidelines.

### Phase 4: Citation Format Conversion (APA → IEEE)
**OpenCode + QA**
*   *Action:* Once the reference list is 100% locked, OpenCode converts Ch6 to numbered `[N]` format and updates every `(Author, Year)` inline citation.
*   *Standard:* QA verifies that the numbering in the text perfectly matches the bibliography order.

### Phase 5: Final Readability and Academic Polish
**QA + Lead**
*   *Action:* QA performs a final read-through of the Persian document for redundancy and academic tone. 
*   *Standard:* Changes are restricted to flow and clarity; no core methodological claims are altered.

### Phase 6: Final Generation
**OpenCode + Lead**
*   *Action:* OpenCode runs the Pandoc pipeline using the university template to generate the final DOCX.
*   *Standard:* Lead reviews the final DOCX visually to ensure formatting, images, and tables rendered correctly before handing off to the student.

---
*Note: The English translation (`ACADEMIC_v3_En.md`) is strictly deferred until Phase 6 is entirely complete on the Persian document.*
