# Framing of the watch report (validated 2026-10-19)

Source of requirements: "Sujet final Veille Cybersecurite Individuel.pdf" (section 1 "Choisir une problématique ciblée"
and section 3, part 2 "Scope and context").

## Watch question (decision-oriented)

Should a French mid-sized SaaS software company let AI coding agents and MCP servers operate on its source code,
CI/CD pipelines and cloud environments, and under which prioritised controls, given what the recent evidence
actually establishes?

## Organisation (fictional, no confidential data)

- French software publisher (SaaS), about 200 developers, about 600 employees.
- Developers use agentic coding assistants (GitHub Copilot, Cursor, Claude Code); a few internal MCP servers are
  connected to Git repositories, the ticketing system and cloud consoles.
- Critical assets: source code, CI/CD secrets, customer-facing production environments, customer data.
- Regulatory context to check (assumptions, not facts): NIS2 applicability, GDPR (CNIL), ANSSI recommendations on
  generative AI. Each must be verified against a primary source before being written in the report.

## Period observed

Active watch: 19 October to 9 November 2026. Baseline events from 2025 to October 2026 are used as background evidence.

## Working hypotheses (to be confirmed OR refuted by the evidence, not assumed)

- H1: indirect prompt injection is the most realistic attack vector against coding agents.
- H2: third-party components (MCP servers, plugins, packages suggested by the model) are the weakest link in the
  software supply chain around these tools.
- H3: available controls (sandboxing, least privilege, human approval of actions) reduce the risk, but vendor defaults
  are not sufficient on their own.
- Divergence to test: French institutional sources (ANSSI, CNIL, CERT-FR) emphasise governance and compliance, while
  English research and vendor sources emphasise concrete exploits. Does this lead to different recommendations?

## Report structure (imposed)

1 Executive summary | 2 Scope and context | 3 Evidence and key findings | 4 Cybersecurity impact assessment |
5 Prioritised recommendations (action, purpose, priority, owner, conditions) | 6 Watch outlook and references |
Methodological annex (1 page max). 6 to 10 pages of content, excluding references and annexes. Fully in English.
