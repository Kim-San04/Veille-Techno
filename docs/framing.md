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

### NIS2 scoping (decision 2026-10-19: define the company so that it falls under NIS2)

NIS2 does not name "software publishers" or "SaaS". The company is therefore described by what it actually does, so
that it matches an Annex I category of Directive (EU) 2022/2555:
- Route A (more robust): besides the SaaS product, it installs, operates, administers and maintains customers'
  applications and environments (managed hosting and maintenance), which fits the definition of a managed service
  provider (Annex I, sector 9 "ICT service management (B2B)"). The definition wording was confirmed on the official
  ANSSI MonEspaceNIS2 help page, not yet on the directive text itself.
- Route B (interpretive): the SaaS platform qualifies as a "cloud computing service" (Annex I, sector 8 "Digital
  infrastructure"). Whether SaaS fits that definition must be checked against Article 6 and the recitals.
- Size: about 600 employees, so above the medium-enterprise ceilings (Recommendation 2003/361). Expected consequence:
  "essential entity" (Article 3), to be confirmed in the text.

Legal status to state accurately (verified only through secondary sources so far, to confirm on primary ones):
France had not transposed NIS2 as of 19 October 2026 (the "loi Résilience" was not adopted; the Assemblée nationale
agenda item of 7 October 2026 was withdrawn on 6 October; the European Commission referred France to the Court of
Justice on 8 July 2026). So: in scope in principle through the directive, but no French obligations in force yet.
Some online guides present the law as already adopted: this divergence between sources is itself evidence to report.

To verify before writing anything about NIS2 in the report (primary sources only):
1. Directive (EU) 2022/2555: Article 2(1), Article 3(1)-(2), Article 6 definitions (cloud computing service, managed
   service provider), Annex I sectors 8 and 9. EUR-Lex blocks scripts: the user must download the official PDF into
   Docs/sources/, then ingest it with `veille add --file`.
2. French legislative status: dossier législatif of the Assemblée nationale (assemblee-nationale.fr).
3. Infringement proceedings: European Commission or CJEU official publication.

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
