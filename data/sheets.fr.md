# Fiches source (brouillons à relire) — traduction française

> Traduction pour lecture uniquement. Les citations (lignes `>`) restent dans la langue d'origine. La version de référence est sheets.md.

## GHSA-pq7j-f95f-qfcv : Claude Code : contournement de l'épinglage par hash des plugins permettant de contourner l'épinglage par hash

- **URL**: https://github.com/advisories/GHSA-pq7j-f95f-qfcv
- **Publisher**: GitHub Advisories (GitHub Advisories (GitHub Advisory Database)) | **Language**: en | **Date**: 2026-10-15
- **Type de source**: primary | **Fiabilité a priori**: 5/5 | **Review**: draft
- **Texte analysé**: full_text | **Citations vérifiées**: 5/5
- **Tags**: claude-code, claude-desktop, plugin-marketplace, supply-chain, git, sha-pinning, integrity-verification, GHSA | **Taxonomy**: Agentic AI supply-chain security > Plugin installation integrity / pinning bypass > Claude Code and Claude Desktop plugin install flow (git checkout) > Installing third-party plugins into AI coding assistants > emerging

**Résumé**
1. L'installation de plugins dans Claude Code/Desktop exécutait un git checkout d'un SHA épinglé sans vérifier que HEAD correspondait à ce SHA.
2. Un attaquant contrôlant le dépôt du plugin pouvait nommer une branche avec le SHA épinglé de 40 caractères.
3. Le checkout se résolvait alors vers la pointe de la branche de l'attaquant, installant du code contrôlé par l'attaquant malgré l'épinglage.
4. L'exploitation nécessite qu'un utilisateur installe un plugin malveillant et qu'un hébergeur git autorise les noms de branche ayant la forme d'un SHA.
5. Classée High (CVSS v4 7.5) ; corrigée, les utilisateurs en mise à jour automatique sont déjà protégés et les utilisateurs en mise à jour manuelle sont invités à mettre à jour.

**Enseignement**: L'épinglage par SHA de commit est souvent considéré comme un contrôle robuste de la chaîne d'approvisionnement pour les plugins et extensions d'agents. Cet avis montre que l'épinglage peut être contourné si l'installateur ne vérifie pas le commit résolu : un hash examiné ne garantit donc pas que le code a été examiné. Les équipes qui utilisent des agents de codage IA avec des marketplaces de plugins doivent traiter l'installation d'un plugin comme une exécution de code sur les postes des développeurs et s'assurer que les outils d'agents sont à jour.

**Action recommandée**: Vérifier que toutes les installations de Claude Code et Claude Desktop sont à la dernière version (en particulier pour les utilisateurs en mise à jour manuelle). Passer en revue les plugins installés depuis des dépôts tiers et vérifier que le HEAD extrait correspond bien au SHA épinglé visé. Intégrer les sources de plugins au processus de revue de la chaîne d'approvisionnement.

**Affirmations clés**
- [fact] ✓ Le flux d'installation des plugins extrayait le SHA de commit épinglé sans vérifier que HEAD correspondait à ce SHA.
  > checked out a marketplace's pinned commit SHA using git checkout without verifying that the resulting HEAD matched the pinned SHA.
- [fact] ✓ Un attaquant contrôlant le dépôt amont pouvait utiliser une branche nommée comme le SHA épinglé pour faire installer du code contrôlé par l'attaquant malgré l'épinglage.
  > An attacker controlling a plugin's upstream repository could create a branch named identically to the pinned 40-character SHA
- [fact] ✓ L'exploitation dépendait d'une action de l'utilisateur et d'un hébergeur git autorisant les noms de branche ayant la forme d'un SHA.
  > Exploitation required a user to install a malicious plugin, pin to a safe hash, and for the plugin source to be hosted on a git host that permitted SHA-shaped branch names.
- [recommendation] ✓ Un correctif a été diffusé ; les utilisateurs en mise à jour automatique l'ont déjà et les utilisateurs en mise à jour manuelle doivent mettre à jour.
  > Users on standard Claude Code auto-update have received this fix already. Users performing manual updates are advised to update to the latest version.
- [fact] ✓ Le problème est classé High, CVSS 7.5, avec un vecteur d'attaque réseau, une faible complexité et une interaction active de l'utilisateur.
  > Severity High 7.5 CVSS overall score

**Notes de fiabilité**: Source primaire : une entrée examinée de la GitHub Advisory Database, la description côté éditeur fait donc probablement autorité. Aucun identifiant CVE n'est indiqué dans le texte ; seul l'identifiant GHSA apparaît dans l'URL. Les détails techniques sont brefs : pas de preuve de concept, pas de numéros de version affectée ou corrigée, et pas de liste des hébergeurs git autorisant les noms de branche ayant la forme d'un SHA. Le texte standard de définition du CVSS n'apporte aucune information sur ce problème. Le rapporteur est mentionné (Or Nevo Michrowski, Air Security), mais les affirmations ne peuvent pas être reproduites de façon indépendante à partir du seul texte. L'éditeur semble être la source de l'avis, d'où un possible conflit d'intérêts, bien que cela ne soit pas indiqué. La date de publication (2026) est tirée du document.

---

## GHSA-9jww-cxg5-rj9m : Nginx UI : MCP `nginx_config_add` contourne la validation des directives — RCE authentifiée

- **URL**: https://github.com/advisories/GHSA-9jww-cxg5-rj9m
- **Publisher**: GitHub Advisories (GitHub Advisories) | **Language**: en | **Date**: 2026-10-15
- **Type de source**: primary | **Fiabilité a priori**: 5/5 | **Review**: draft
- **Texte analysé**: full_text | **Citations vérifiées**: 7/7
- **Tags**: MCP, Nginx UI, RCE, authentication, directive validation bypass, agentic tooling, supply chain, infrastructure security | **Taxonomy**: AI agent security > MCP tool implementation vulnerabilities > Model Context Protocol (MCP) > Infrastructure management / nginx configuration via AI agent tooling > emerging

**Résumé**
1. L'outil MCP nginx_config_add écrit des fichiers de configuration nginx et recharge nginx sans appeler config.ValidateConfigFile.
2. Le point de terminaison REST équivalent (POST /api/configs) appelle bien cette validation et bloque les directives dangereuses.
3. Des directives bloquées telles que perl, js_import, load_module et user root peuvent être écrites via le chemin MCP.
4. Les points de terminaison MCP acceptent les mêmes jetons JWT/node-secret que l'API REST, ce qui rend exploitable toute session authentifiée.
5. Une preuve de concept (PoC) montre l'écriture d'une directive perl via MCP, permettant l'exécution de commandes arbitraires sous l'utilisateur worker de nginx.

**Enseignement**: Cet avis montre qu'un plan de contrôle destiné aux IA/agents (MCP) pour un outil d'infrastructure peut omettre silencieusement des contrôles de sécurité présents dans l'API REST équivalente destinée aux humains, créant une surface d'attaque parallèle et moins testée. Pour les équipes qui intègrent des agents de codage/d'exploitation basés sur MCP, cela démontre que chaque outil MCP doit être audité indépendamment : la parité fonctionnelle avec REST n'implique pas la parité de sécurité, et des agents pourraient être trompés ou détournés pour invoquer des outils MCP insuffisamment validés, menant à une RCE.

**Action recommandée**: Auditer toutes les implémentations d'outils MCP afin de vérifier leur parité avec la logique de validation de l'API REST (en particulier pour les opérations d'écriture ou déclenchant un rechargement) ; corriger config_add.go pour appeler ValidateConfigFile avant l'écriture ; traiter les points de terminaison MCP comme une surface d'attaque distincte et auditable dans les revues de sécurité des outils agentiques ; restreindre ou surveiller l'usage des jetons MCP de nginx-ui jusqu'à la correction.

**Affirmations clés**
- [fact] ✓ The MCP tool nginx_config_add writes config files and reloads nginx without calling the validation function used by the REST API.
  > The MCP tool nginx_config_add writes nginx configuration files to disk and triggers an nginx reload without calling config.ValidateConfigFile.
- [fact] ✓ The REST API endpoint POST /api/configs correctly calls ValidateConfigFile and rejects dangerous directives.
  > The identical flow in the REST API (POST /api/configs) does call that function and correctly rejects dangerous directives.
- [fact] ✓ Only config_add.go is affected; config_modify.go correctly validates.
  > Note that mcp/config/config_modify.go does call ValidateConfigFile correctly — only config_add.go is affected.
- [fact] ✓ MCP endpoints accept the same authentication tokens as the REST API, making the attack surface any authenticated session.
  > The MCP endpoint (GET /mcp SSE + POST /mcp_message JSON-RPC) accepts the same JWT and node-secret tokens as the REST API, so the attack surface is any authenticated session.
- [analysis] ✓ On servers with Perl or njs modules loaded, this bypass leads to post-authentication remote code execution.
  > On a server with the nginx Perl, njs, or Lua module loaded, this is post-authentication Remote Code Execution.
- [fact] ✓ A proof-of-concept demonstrates writing a perl directive via the MCP tool that is rejected by the REST API but accepted via MCP, enabling command execution.
  > The perl directive — explicitly listed in blockedConfigDirectives and rejected by the REST API — passes through without any check.
- [hypothesis] ✓ Combining this bypass with a user root directive could allow escalation to root before the RCE handler fires.
  > Combined with a user root; directive (also unblocked via this path), the worker process can be escalated to root before the RCE handler fires.

**Notes de fiabilité**: Il s'agit d'un avis de sécurité de source primaire (GitHub Advisories) comportant un PoC détaillé et reproductible, avec les charges utiles de requête/réponse et des références de lignes de code, ce qui renforce sa crédibilité. Toutefois, il s'agit d'une divulgation unique issue de l'écosystème de l'éditeur, sans confirmation tierce indépendante dans ce document ; aucun identifiant CVE n'est fourni, et certains détails (par ex. les numéros de version corrigée exacts, la plage de versions affectées) ne figurent pas dans le texte fourni. Aucun conflit d'intérêts n'est apparent, mais l'affirmation d'une élévation vers root via la combinaison avec la directive « user root » est présentée comme une hypothèse/extension plutôt que comme une démonstration directe dans le PoC.

---

## GHSA-76pm-mq2q-9gcr: Nginx UI: l'outil MCP nginx_config_add ignore la validation des directives de configuration → injection authentifiée de directives nginx (RCE sur l'image officielle)

- **URL**: https://github.com/advisories/GHSA-76pm-mq2q-9gcr
- **Publisher**: GitHub Advisories (GitHub Advisories) | **Language**: en | **Date**: 2026-10-15
- **Type de source**: primary | **Fiabilité a priori**: 5/5 | **Review**: draft
- **Texte analysé**: full_text | **Citations vérifiées**: 7/7
- **Tags**: MCP, nginx-ui, RCE, prompt injection, directive injection, Docker, privilege escalation, AI agent security | **Taxonomy**: AI agent security > MCP tool validation bypass > Model Context Protocol (MCP) > AI-driven infrastructure/config management > emerging

**Résumé**
1. mcp/config/config_add.go écrit directement sur le disque le contenu de configuration nginx fourni via MCP, sans appeler ValidateConfigFile, contrairement aux chemins équivalents.
2. Cela permet d'injecter des directives bloquées (js_*, perl_*, load_module, user root) via l'outil MCP nginx_config_add.
3. Une preuve de concept réelle contre l'image Docker officielle uozi/nginx-ui:2.3.11 démontre le chargement du module njs et l'élévation de privilèges vers root.
4. La faille provient d'un commit de durcissement incomplet (3e411d38) qui a corrigé trois des quatre chemins d'écriture de configuration mais a omis config_add.go.
5. Le problème est distinct d'un CVE précédemment corrigé concernant un endpoint MCP non authentifié et nécessite une authentification (secret de nœud ou JWT), éventuellement via un agent IA victime d'une injection de prompt.

**Enseignement**: Ce cas illustre un schéma de risque concret et reproductible pour les agents IA de développement/exploitation connectés à des outils MCP : les contrôles de sécurité appliqués sur certains chemins de code invoqués par les outils peuvent être silencieusement absents des chemins voisins, et un agent authentifié — y compris manipulé par injection de prompt — peut servir de vecteur pour contourner la validation des directives et obtenir une exécution de code au niveau root. Il souligne que les surfaces d'outils MCP doivent être auditées chemin par chemin pour garantir une application cohérente des contrôles de sécurité, et pas seulement au niveau de la couche API, et que l'accès d'agents à des outils modifiant l'infrastructure multiplie l'impact d'un simple appel de validation manquant.

**Action recommandée**: Corriger mcp/config/config_add.go pour appeler config.ValidateConfigFile(path, content) avant os.WriteFile, conformément à la validation déjà présente dans config_modify.go et dans les chemins de l'API ; auditer tous les gestionnaires d'outils MCP pour vérifier l'application cohérente des contrôles de sécurité ; restreindre ou surveiller l'accès des agents MCP aux outils d'écriture de configuration, en particulier dans les déploiements embarquant les modules njs/perl.

**Affirmations clés**
- [fact] ✓ L'outil MCP nginx_config_add n'appelle pas ValidateConfigFile, contrairement aux autres chemins d'écriture de configuration.
  > The fourth path — the MCP tool nginx_config_add (mcp/config/config_add.go) — does NOT call it: it writes the caller-supplied content straight to disk and reloads nginx.
- [analysis] ✓ La cause racine est un commit de durcissement incomplet qui a omis ce chemin.
  > It did NOT touch mcp/config/config_add.go. So the MCP add path was left without the validation that all of its sibling paths received.
- [fact] ✓ Une preuve de concept réelle contre l'image Docker officielle a permis une exécution de code root via le chargement du module njs et la directive user root.
  > /proc/<worker>/status → Uid: 0 0 0 0 (workers run as root — user root took effect).
- [hypothesis] ✓ La vulnérabilité peut être déclenchée par un appelant MCP authentifié ou par un agent IA détourné via injection de prompt.
  > An authenticated MCP principal — or a connected AI agent subverted via prompt injection — bypasses the directive-validation security control and injects directives the project explicitly blocks elsewhere.
- [analysis] ✓ Sur un nginx standard sans modules njs/perl, l'impact se réduit à un déni de service et à une régression de privilèges.
  > On stock nginx without those modules it is a reliable DoS (failed reload) plus a user root privilege regression.
- [recommendation] ✓ Le correctif suggéré est d'appeler ValidateConfigFile avant d'écrire le fichier, comme sur le chemin voisin.
  > Call config.ValidateConfigFile(path, content) in handleNginxConfigAdd before os.WriteFile, matching mcp/config/config_modify.go and the API paths
- [fact] ✓ Ce problème est distinct d'un CVE précédemment identifié concernant un endpoint MCP non authentifié.
  > Distinct from CVE-2026-33032 (GHSA-h6c2-x2m2-mwhf, "Unauthenticated MCP Endpoint"), whose root cause is a MISSING AUTH middleware on /mcp_message

**CVE**: verified ['CVE-2026-33032'] | rejected []

**Notes de fiabilité**: Il s'agit d'un avis de sécurité de source primaire, accompagné d'une preuve de concept détaillée et reproductible incluant les commandes exactes, des diffs de code et des preuves au niveau des fichiers (UID du worker, fichier de preuve créé), ce qui renforce la crédibilité technique. Cependant, il s'agit d'une divulgation de vulnérabilité auto-déclarée (probablement par un chercheur indépendant plutôt que par l'éditeur) ; les affirmations de ce document ne font donc l'objet d'aucune confirmation indépendante, et aucune réponse de l'éditeur ni confirmation de correctif n'est incluse. Les limites de portée sont explicitement indiquées par l'auteur, ce qui améliore la transparence, mais la fiabilité globale dépend d'une vérification par les mainteneurs de nginx-ui, qui n'est pas mentionnée dans le document.

---

## CVE-2025-71427: Office-PowerPoint-MCP-Server through 2.0.7 contains a path traversal vulnerability that allows MCP callers to write and

- **URL**: https://nvd.nist.gov/vuln/detail/CVE-2025-71427
- **Publisher**: NVD (CVE) (NVD (National Vulnerability Database)) | **Language**: en | **Date**: 2026-10-01
- **Type de source**: primary | **Fiabilité a priori**: 5/5 | **Review**: draft
- **Texte analysé**: stored_summary | **Citations vérifiées**: 4/4
- **Tags**: MCP, path traversal, prompt injection, CVE-2025-71427, file write, AI agents, Office-PowerPoint-MCP-Server | **Taxonomy**: MCP ecosystem vulnerabilities > Path traversal in MCP server tools > Office-PowerPoint-MCP-Server > AI agent file handling and document generation via MCP > emerging

**Résumé**
1. Office-PowerPoint-MCP-Server jusqu'à la version 2.0.7 présente une vulnérabilité de path traversal.
2. Les appelants MCP peuvent lire et écrire des fichiers en dehors du répertoire de travail via des chemins absolus ou des séquences ../.
3. Fonctions concernées : save_presentation, open_presentation et manage_image output_path.
4. Des attaquants peuvent recourir à une injection de prompt pour pousser un agent IA à abuser de ces fonctions.
5. Impact : écrasement de tout fichier accessible en écriture par le serveur ou chargement de fichiers externes ; l'état du correctif et le score CVSS ne sont pas indiqués.

**Enseignement**: Il s'agit d'un exemple concret de serveur MCP exposant des outils de système de fichiers sans confinement des chemins : un agent victime d'une injection de prompt devient alors un relais de lecture/écriture arbitraire de fichiers. Pour une équipe qui utilise des agents de codage IA avec des serveurs MCP, cela montre que les arguments d'outils produits par le modèle doivent être traités comme des entrées non fiables, et que la validation des chemins côté serveur compte autant que les défenses côté modèle.

**Action recommandée**: Inventorier l'utilisation éventuelle d'Office-PowerPoint-MCP-Server (version 2.0.7 ou antérieure) ; si c'est le cas, le restreindre ou le retirer, l'exécuter dans un bac à sable ou avec des permissions minimales sur le système de fichiers, et vérifier l'existence d'une version corrigée (non indiquée dans le document). Plus généralement, examiner les serveurs MCP afin de vérifier le confinement des chemins dans les outils de gestion de fichiers.

**Affirmations clés**
- [fact] ✓ Office-PowerPoint-MCP-Server jusqu'à la version 2.0.7 contient une vulnérabilité de path traversal permettant la lecture et l'écriture de fichiers en dehors du répertoire de travail.
  > Office-PowerPoint-MCP-Server through 2.0.7 contains a path traversal vulnerability that allows MCP callers to write and read files outside the working directory
- [fact] ✓ Le traversal est déclenché en fournissant des chemins absolus ou des séquences ../.
  > by supplying absolute paths or ../ sequences
- [fact] ✓ Des attaquants peuvent utiliser une injection de prompt pour pousser un agent IA à abuser de save_presentation, open_presentation ou manage_image output_path.
  > Attackers can steer an AI agent via prompt injection to abuse save_presentation, open_presentation, or manage_image output_path
- [fact] ✓ L'exploitation peut écraser tout fichier accessible en écriture par le serveur ou charger des fichiers externes.
  > to overwrite any server-writable file or load external files.

**CVE**: verified ['CVE-2025-71427'] | rejected []

**Notes de fiabilité**: Source primaire (NVD), mais le texte n'est qu'un résumé stocké. Il ne fournit ni score CVSS, ni version corrigée, ni preuve de concept, ni information sur une exploitation dans la nature (tous non indiqués). La description semble provenir de l'enregistrement CVE, dont le déclarant d'origine n'est pas indiqué. Le scénario d'attaque par injection de prompt est décrit mais ni démontré ni reproductible à partir de ce texte. La date de publication (2026-10-01) est celle fournie dans les métadonnées.

---

## CVE-2026-53509: CKAN MCP Server is a tool for querying CKAN open data portals. A known vulnerability CVE-2026-33060 indicated tools incl

- **URL**: https://nvd.nist.gov/vuln/detail/CVE-2026-53509
- **Publisher**: NVD (CVE) (NVD (NIST National Vulnerability Database)) | **Language**: en | **Date**: 2026-08-21
- **Type de source**: primary | **Fiabilité a priori**: 5/5 | **Review**: draft
- **Texte analysé**: stored_summary | **Citations vérifiées**: 5/5
- **Tags**: MCP, SSRF, CKAN, input validation, filter bypass, CVE, loopback, incomplete fix | **Taxonomy**: MCP ecosystem vulnerabilities > Server-side request forgery in MCP tool servers > CKAN MCP Server (src/utils/http.ts) > Agent/MCP tools querying external open data portals > emerging

**Résumé**
1. CKAN MCP Server interroge des portails de données ouvertes CKAN et accepte des URL de serveur fournies par l'appelant.
2. Un problème SSRF antérieur (CVE-2026-33060) avait été corrigé par un filtrage des adresses IP.
3. Le filtre ne vérifiait que la chaîne du nom d'hôte analysé, de sorte que des alias comme ip6-localhost passaient.
4. Un appelant MCP distant pouvait faire accéder le serveur à des adresses locales ou privées et lire des réponses de forme CKAN.
5. La version 0.4.106 a remplacé la vérification unique de localhost par un Set de noms d'hôte bloqués.

**Enseignement** : Les serveurs MCP qui récupèrent des URL fournies par l'appelant constituent des surfaces SSRF, et un agent IA ou un appelant distant qui invoque leurs outils peut atteindre les réseaux internes depuis la position du serveur. Le filtrage des noms d'hôte par chaînes de caractères est fragile : des alias résolus vers la boucle locale ont contourné un correctif antérieur. Une équipe de développement utilisant des agents de codage avec des serveurs MCP doit traiter les paramètres d'URL des outils comme des entrées non fiables et vérifier les contrôles au niveau réseau, pas seulement la logique de validation.

**Action recommandée** : Inventoriez les déploiements de CKAN MCP Server et passez à la version 0.4.106 ou ultérieure. Plus généralement, examinez les serveurs MCP qui acceptent des paramètres d'URL, et ajoutez des restrictions de sortie (egress) ou une validation de l'IP résolue plutôt que de vous fier à des vérifications de chaînes de noms d'hôte. Notez que le correctif décrit dans le document est une liste de blocage : refaites donc des tests après la mise à niveau.

**Affirmations clés**
- [fact] ✓ The earlier fix for CVE-2026-33060 filtered IP addresses but could be bypassed in versions prior to 0.4.106.
  > A fix was applied to filter out ip addresses. However, a method to bypass exists prior to version 0.4.106.
- [fact] ✓ The server validated caller-supplied CKAN URLs by inspecting only the parsed hostname string before making outbound requests.
  > CKAN MCP Server validates caller-supplied CKAN server URLs by inspecting only the parsed hostname string before issuing outbound HTTP requests.
- [fact] ✓ Hostname aliases such as ip6-localhost passed the SSRF filter but could resolve to loopback.
  > hostname aliases such as `ip6-localhost` are not equal to `localhost`, are not dotted IPv4 literals, and are not bracketed IPv6 literals, so they pass the SSRF filter
- [analysis] ✓ A remote MCP caller able to invoke CKAN tools could make the server connect to local or private addresses and receive response-derived data for CKAN-shaped responses.
  > A remote MCP caller that can invoke CKAN tools with a `server_url` can therefore make the server connect to local or private addresses
- [fact] ✓ Version 0.4.106 replaced the single localhost check with a blocked-hostname Set covering ip6-localhost and ip6-loopback.
  > replaced the single `hostname === 'localhost'` check with a blocked-hostname `Set` covering `ip6-localhost` and `ip6-loopback`.

**CVE**: verified ['CVE-2026-33060'] | rejected []

**Notes de fiabilité** : Enregistrement NVD primaire, mais il s'agit d'un résumé stocké, probablement issu de l'avis du fournisseur ou du mainteneur. CVE-2026-33060 apparaît dans le texte ; l'identifiant propre à la page (CVE-2026-53509) n'apparaît que dans l'URL, pas dans le corps du document, il n'est donc pas listé. Aucun score CVSS, preuve de concept ou étape de reproduction n'est indiqué. Le correctif est une liste de blocage de noms d'hôte, qui peut rester incomplète (par exemple autres alias ou résolution via DNS), mais le document ne le dit pas. Le texte mentionne à la fois un paramètre `server_url` et un paramètre `base_url` sans les réconcilier.

---

## CVE-2025-66416: The MCP Python SDK, called `mcp` on PyPI, is a Python implementation of the Model Context Protocol (MCP). Prior to versi

- **URL**: https://nvd.nist.gov/vuln/detail/CVE-2025-66416
- **Publisher**: NVD (CVE) (NVD (National Vulnerability Database)) | **Language**: en | **Date**: 2025-12-02
- **Type de source**: primary | **Fiabilité a priori**: 5/5 | **Review**: draft
- **Texte analysé**: stored_summary | **Citations vérifiées**: 6/6
- **Tags**: MCP, Python SDK, DNS rebinding, FastMCP, SSE, streamable HTTP, localhost, same-origin policy, CVE-2025-66416 | **Taxonomy**: MCP ecosystem vulnerabilities > Insecure default configuration of local MCP servers > MCP Python SDK (mcp on PyPI), FastMCP > Running local HTTP-based MCP servers for AI assistants and coding agents > established

**Résumé**
1. Le SDK Python MCP (`mcp` sur PyPI) antérieur à la version 1.23.0 n'active pas par défaut la protection contre le DNS rebinding pour les serveurs basés sur HTTP.
2. Configuration concernée : serveur localhost, sans authentification, FastMCP avec HTTP streamable ou SSE, sans TransportSecuritySettings configuré.
3. Un site web malveillant pourrait utiliser le DNS rebinding pour contourner la same-origin policy et envoyer des requêtes au serveur MCP local.
4. Un attaquant pourrait invoquer des outils ou accéder à des ressources exposés par le serveur au nom de l'utilisateur, dans des circonstances limitées.
5. Les serveurs utilisant le transport stdio ne sont pas affectés ; le problème est corrigé dans la version 1.23.0.

**Enseignement**: Les développeurs qui exécutent des serveurs MCP locaux pour des agents de codage IA peuvent exposer des outils et des ressources à n'importe quel site web visité par l'utilisateur si le serveur utilise le transport HTTP/SSE sans authentification et sans protection contre le DNS rebinding. Comme les outils MCP peuvent effectuer des actions (fichiers, commandes, accès aux données), une attaque pilotée par le navigateur contre un serveur localhost constitue une voie réaliste d'abus de la surface d'outils de l'agent. Mettre à jour le SDK, ajouter une authentification et privilégier stdio réduisent ce risque.

**Action recommandée**: Inventorier les serveurs MCP locaux construits avec le SDK Python ; mettre à niveau `mcp` vers la version 1.23.0 ou ultérieure ; pour les serveurs HTTP/SSE, configurer TransportSecuritySettings et ajouter une authentification ; privilégier le transport stdio pour un usage local.

**Affirmations clés**
- [fact] ✓ Les versions du SDK Python MCP antérieures à 1.23.0 n'activent pas par défaut la protection contre le DNS rebinding pour les serveurs basés sur HTTP.
  > Prior to version 1.23.0, tThe Model Context Protocol (MCP) Python SDK does not enable DNS rebinding protection by default for HTTP-based servers.
- [fact] ✓ L'exploitation nécessite un serveur FastMCP localhost, non authentifié, utilisant HTTP streamable ou SSE sans TransportSecuritySettings configuré.
  > When an HTTP-based MCP server is run on localhost without authentication using FastMCP with streamable HTTP or SSE transport, and has not configured TransportSecuritySettings
- [fact] ✓ Un site web malveillant pourrait utiliser le DNS rebinding pour contourner la same-origin policy et atteindre le serveur MCP local.
  > a malicious website could exploit DNS rebinding to bypass same-origin policy restrictions and send requests to the local MCP server.
- [analysis] ✓ L'impact est qu'un attaquant pourrait invoquer des outils ou accéder à des ressources au nom de l'utilisateur, dans des circonstances limitées.
  > This could allow an attacker to invoke tools or access resources exposed by the MCP server on behalf of the user in those limited circumstances.
- [fact] ✓ L'exécution locale de serveurs MCP basés sur HTTP sans authentification est déconseillée par les bonnes pratiques de sécurité MCP.
  > Note that running HTTP-based MCP servers locally without authentication is not recommended per MCP security best practices.
- [fact] ✓ Les serveurs basés sur stdio ne sont pas affectés, et la version 1.23.0 corrige le problème.
  > This issue does not affect servers using stdio transport. This vulnerability is fixed in 1.23.0.

**CVE**: verified ['CVE-2025-66416'] | rejected []

**Notes de fiabilité**: Source primaire (fiche NVD), mais le texte est un résumé stocké de la description fournie par l'éditeur ; il contient une coquille (« tThe »). Aucun score CVSS, preuve de concept, élément d'exploitation ni détail technique du correctif n'est indiqué. La formulation « circonstances limitées » suggère une exposition restreinte, mais la prévalence réelle des configurations affectées n'est pas précisée.

---

## LaTeX renderer

- **URL**: https://simonwillison.net/2026/Oct/15/latex/
- **Publisher**: Simon Willison (Simon Willison) | **Language**: en | **Date**: 2026-10-15
- **Type de source**: secondary | **Fiabilité a priori**: 4/5 | **Review**: draft
- **Texte analysé**: full_text | **Citations vérifiées**: 5/5
- **Tags**: agentic-coding, claude-code, xss, iframe-sandbox, dompurify, llms.txt, latex, url-fragment | **Taxonomy**: AI coding agent practice > Agent-generated web tools and XSS mitigation > Claude Code, MathJax, DOMPurify, iframe sandbox > Building a shareable LaTeX renderer with a coding agent > emerging

**Résumé**
1. L'auteur s'est inspiré de Tiny Little Office, qui stocke les données du document dans le #fragment de l'URL.
2. Tiny Little Office fournit aussi un llms.txt indiquant aux agents comment construire des URL de documents affichables.
3. L'auteur a demandé à Claude Code (Opus 5.5 Extra) de construire un moteur de rendu LaTeX similaire à l'aide d'une courte série de prompts.
4. Les prompts demandaient une protection contre les XSS via un iframe sandbox ainsi qu'une fonctionnalité de chargement depuis une URL/un Gist, toutes deux copiées d'un outil existant.
5. L'outil utilise Pako 2.1.0, MathJax 4.1.3, faster-latex 0.3.1 et DOMPurify 3.4.16.

**Enseignement**: L'article montre un flux de travail léger où un agent de codage IA construit un outil qui affiche du contenu non fiable (LaTeX provenant d'un fragment d'URL, d'une URL ou d'un Gist). La sécurité n'est abordée qu'en demandant dans les prompts un iframe sandbox et DOMPurify, et aucune revue ni aucun test de cette protection n'est décrit. Pour une équipe qui utilise des agents de codage, cela illustre que les contrôles de sécurité sont souvent demandés de manière ad hoc dans les prompts, et que le contenu intégré dans les fragments ainsi que les fichiers llms.txt lisibles par les agents sont des canaux d'entrée nécessitant une attention particulière.

**Action recommandée**: Non indiquée par l'auteur. Suggestion pour le fichier de veille : lorsque des agents génèrent des outils qui affichent du contenu contrôlé par l'utilisateur, revoir indépendamment la configuration du sandbox et de l'assainissement (attributs iframe sandbox, utilisation de DOMPurify, chargement distant d'URL/Gist) plutôt que de se fier au seul prompt.

**Affirmations clés**
- [fact] ✓ Tiny Little Office stocke toutes les données du document dans le fragment de l'URL, ce qui fait de chaque document un lien partageable et pouvant être mis en favori.
  > Tiny Little Office's signature trick is to store all of the document data in the #fragment section of the URL, so every document created using it becomes a bookmarkable and shareable link.
- [fact] ✓ Tiny Little Office fournit un fichier llms.txt qui indique aux agents comment construire des URL qui s'affichent comme des documents.
  > It also has an llms.txt file telling agents how to construct URLs that will render as documents.
- [fact] ✓ L'auteur a utilisé Claude Code (Opus 5.5 Extra) pour construire un outil LaTeX similaire.
  > Tiny Little Office inspired me to have Claude Code (Opus 5.5 Extra) build a similar tool that works with LaTeX.
- [fact] ✓ L'auteur a demandé à l'agent d'utiliser un iframe sandbox, comme dans un outil existant, pour se protéger des risques de XSS.
  > Since it was working in my tools repo I told it to take inspiration from the <iframe sandbox="..."> mechanism used by my existing SVG in Markdown tool as protection against XSS risks:
- [fact] ✓ L'outil dépend de Pako, MathJax, faster-latex et DOMPurify dans des versions précises.
  > The tool uses Pako 2.1.0, MathJax 4.1.3, faster-latex 0.3.1, and DOMPurify 3.4.16.

**Notes de fiabilité**: Source secondaire : un billet de blog personnel d'un seul auteur décrivant son propre projet. C'est une description courte, sans test de sécurité, sans modèle de menaces et sans preuve que le sandbox empêche effectivement les XSS. Les prompts complets et le code ne figurent pas dans le texte, de sorte que le résultat ne peut pas être reproduit à partir de ce seul document. Les liens vers l'outil et le lien d'exemple ne sont pas visibles dans le texte fourni. Les affirmations sur Tiny Little Office sont de seconde main et non vérifiées ici. Le nom du modèle et les numéros de version sont donnés tels qu'indiqués par l'auteur et n'ont pas été vérifiés de manière indépendante.

---

## Auditing in the age of (good enough) AI

- **URL**: https://blog.trailofbits.com/2026/09/18/auditing-in-the-age-of-good-enough-ai/
- **Publisher**: Trail of Bits (Trail of Bits) | **Language**: en | **Date**: 2026-09-18
- **Type de source**: secondary | **Fiabilité a priori**: 4/5 | **Review**: draft
- **Texte analysé**: full_text | **Citations vérifiées**: 8/8
- **Tags**: agentic-coding, security-audit, static-analysis, formal-verification, Lean, Claude, Codex, zkVM, case-study | **Taxonomy**: AI-assisted security auditing > Agent-generated tooling and formal proofs > Claude, Codex, Lean, abstract interpretation, LSP > Pre-audit tooling and verification of a zkVM core library > emerging

**Résumé**
1. Trail of Bits a utilisé des agents d'IA pendant six mois pour construire des outils sur mesure avant d'auditer la zkVM Miden.
2. Les agents ont construit un serveur LSP, un décompilateur, un moteur d'analyse statique par interprétation abstraite et un modèle Lean de l'exécuteur de la VM.
3. L'analyse statique a signalé plus de 400 emplacements de validation de types et une valeur advice sous-contrainte de sévérité élevée dans mod_12289.
4. Le travail en Lean a produit 95 preuves vérifiées par machine et deux bogues non détectés par les tests unitaires (rotr, wrapping_mul).
5. Les auteurs soutiennent que les agents rendent désormais les projets annexes exploratoires assez peu coûteux pour qu'un échec ne coûte que des tokens.

**Enseignement**: L'article montre que les agents de codage IA peuvent servir au-delà de la revue de code, pour générer des outils d'analyse sur mesure et des preuves formelles pour des langages de niche, les humains auditant les productions (par ex. uniquement les énoncés des théorèmes, puisque le noyau Lean vérifie les preuves). Pour une équipe de développement, cela suggère un schéma : utiliser des boucles de développement/revue croisées entre modèles, des tests de régression issus de comparaisons aléatoires, et exposer les outils conçus par les agents via des CLI pour les workflows d'agents. Il souligne aussi l'importance de vérifier les entrées fournies par le prouveur ou non fiables. Il n'aborde pas directement les risques de sécurité liés aux agents ou à MCP.

**Action recommandée**: À noter comme étude de cas d'outillage de sécurité conçu par des agents et de vérification formelle. Pour évaluer le risque du codage agentique, le considérer comme une preuve d'usage productif (et de la nécessité de revoir les spécifications/théorèmes générés), non comme une preuve sur la surface d'attaque. Rechercher une validation indépendante des constats sur Miden et des outils.

**Affirmations clés**
- [fact] ✓ Des agents ont construit un serveur LSP, un décompilateur, un moteur d'analyse statique et un modèle Lean sur six mois pour préparer la revue de la VM Miden.
  > we spent six months having our agents build an LSP server, a decompiler, a static analysis engine, and a Lean model of the VM executor from scratch.
- [fact] ✓ Les outils ont trouvé un problème de sévérité élevée permettant à un prouveur malveillant de forger des signatures Falcon.
  > an unvalidated prover-supplied input that would let a malicious prover forge Falcon signatures and steal funds from Miden account holders.
- [fact] ✓ Les analyses ont identifié plus de 400 emplacements où la validation de types pourrait être améliorée, tous atteignables depuis l'API publique, ainsi qu'un constat de sévérité élevée.
  > these analyses identified over 400 unique locations2 where type validation could be improved (all of them reachable from the public API of the library) as well as one high-severity finding.
- [fact] ✓ La modélisation en Lean pilotée par agents a produit 95 preuves de correction et trouvé deux bogues que les tests unitaires avaient manqués.
  > Our agent-driven formal modeling efforts resulted in 95 correctness proofs that covered all of the binary arithmetic components of the core library.
- [analysis] ✓ Seuls les énoncés des théorèmes nécessitaient un audit manuel, car le noyau Lean valide les preuves.
  > Since the Lean kernel could validate that the generated proofs were correct, we only needed to manually audit the theorem statements
- [analysis] ✓ La principale valeur réutilisable du décompilateur résidait dans ses cadres d'analyse et son IR plutôt que dans la décompilation complète.
  > The main benefit of this work turned out to be the decompiler’s internal analysis frameworks and intermediate representation
- [analysis] ✓ Les agents sont devenus assez bons pour porter des projets non essentiels avec une supervision légère, ce qui change l'économie des projets annexes.
  > over the last year, agents became good enough to carry non-essential projects like these with only light supervision, which completely changed the economics
- [fact] ✓ L'équipe Miden a adopté le moteur d'analyse statique pour les futures mises à jour.
  > The team has adopted the static analysis engine developed for the review, which means that our side project will now also help secure future updates

**Notes de fiabilité**: Blog d'un fournisseur décrivant sa propre mission et ses méthodes, sur un ton commercial (appel à prendre contact). Les constats ne sont pas vérifiés de façon indépendante ; aucun code, publication d'outil, détail d'exploitation, taux de faux positifs, ni chiffre de coût ou de durée n'est fourni. L'affirmation « could have led to millions of dollars in lost funds » n'est pas quantifiée. La description de l'interprétation abstraite est simplifiée. N'aborde pas les risques de sécurité liés aux agents ou à MCP. La formulation originale du théorème Lean est absente du texte (exemple omis).

---

## OWASP GenAI Security Project Unveils 2026 Top 10 for LLM Applications, New Agent Control Standard and Sponsors as Community Tops 30,000 Members

- **URL**: https://genai.owasp.org/2026/09/01/owasp-genai-security-project-unveils-2026-top-10-for-llm-applications-new-agent-control-standard-and-sponsors-as-community-tops-30000-members/?utm_source=rss&utm_medium=rss&utm_campaign=owasp-genai-security-project-unveils-2026-top-10-for-llm-applications-new-agent-control-standard-and-sponsors-as-community-tops-30000-members
- **Publisher**: OWASP GenAI (OWASP GenAI Security Project) | **Language**: en | **Date**: 2026-09-01
- **Type de source**: primaire | **Fiabilité a priori**: 4/5 | **Review**: draft
- **Texte analysé**: full_text | **Citations vérifiées**: 7/7
- **Tags**: OWASP, LLM Top 10, agentic AI, Excessive Agency, Agent Control Standard, runtime enforcement, framework mapping, press release | **Taxonomy**: AI security governance and standards > Risk taxonomies for LLM and agentic applications > LLM applications and autonomous agents > Risk prioritization and control design for agentic AI deployments > emerging

**Résumé**
1. OWASP GenAI a publié le Top 10 2026 pour les applications LLM, avec des classements mis à jour et des correspondances avec NIST, MITRE ATLAS et CWE.
2. Selon le projet, cette édition s'appuie sur des recherches issues de milliers d'incidents réels de sécurité de l'IA.
3. L'Agent Control Standard (ACS) a été donné au projet afin d'étendre les recommandations vers l'application des contrôles à l'exécution.
4. Un répertoire élargi de solutions de sécurité de l'IA et un GenAI Security Industry Framework Crosswalk ont été annoncés.
5. Excessive Agency est indiqué (par la citation d'un sponsor) comme se classant au troisième rang ; quatre nouveaux sponsors ont rejoint le projet et le nombre de membres a dépassé 30 000.

**Enseignement**: Pour les équipes qui utilisent des agents de codage IA, cette publication indique que la sur-attribution de permissions aux agents (Excessive Agency) est priorisée par la communauté et par les données d'incidents, et que les recommandations évoluent vers des contrôles applicables à l'exécution sur ce que les agents peuvent consulter et faire. L'ACS et les crosswalks de frameworks pourraient aider à faire correspondre les contrôles des agents aux référentiels de conformité existants, mais l'annonce ne fournit aucun détail technique.

**Action recommandée**: Télécharger le Top 10 LLM 2026 et examiner l'entrée Excessive Agency ainsi que le Top 10 for Agentic Applications ; évaluer les permissions des agents de codage (outils, serveurs MCP, accès aux fichiers et au réseau) au regard de ces documents. Suivre l'ACS pour son contenu technique avant de s'y fier, car le communiqué de presse ne décrit pas ses contrôles.

**Affirmations clés**
- [fact] ✓ Le OWASP GenAI Security Project a publié le Top 10 2026 pour les applications LLM, nouvelle édition de ses recommandations phares.
  > The OWASP GenAI Security Project’s Top 10 for LLM Applications 2026 is the latest edition of the project’s flagship guidance
- [fact] ✓ L'édition 2026 intègre des recherches issues de milliers d'incidents réels et élargit les correspondances avec NIST, MITRE ATLAS, CWE et le Top 10 for Agentic Applications.
  > incorporates updated rankings, expanded threat coverage and research drawn from thousands of real-world AI security incidents.
- [fact] ✓ L'Agent Control Standard a été donné au projet afin d'étendre les recommandations vers une application pratique des contrôles à l'exécution.
  > The Agent Control Standard (ACS) has been donated to the OWASP GenAI Security Project.
- [fact] ✓ Excessive Agency se classe désormais au troisième rang, selon un dirigeant de Zenity, qui affirme que les données d'incidents et le jugement d'experts concordent sur ce point.
  > the risk where expert judgment and the record agree most clearly is Excessive Agency, now number three.
- [recommendation] ✓ La sécurité devrait partir du principe que l'IA échouera ou sera parfois trompée, et placer des contrôles applicables autour de ce que les systèmes peuvent consulter, décider et faire.
  > assuming AI will sometimes fail or be fooled and putting enforceable controls around what these systems can access, decide and do.
- [analysis] ✓ L'IA agentique déplace la question de sécurité de ce qu'un modèle peut dire vers ce qu'un système peut faire.
  > Agentic AI changes the security question from what a model can say to what a system can do.
- [analysis] ✓ De nouveaux types d'actifs tels que les connecteurs, les skills et les plugins introduisent de nouvelles vulnérabilités touchant les équipes transverses.
  > New vulnerabilities and risks are emerging that affect cross-functional teams, and new asset types (eg connectors, skills, plugins).

**Notes de fiabilité**: Communiqué de presse émis par le projet lui-même, avec des citations promotionnelles de sponsors et de fournisseurs (Palo Alto Networks, WitnessAI, Zenity, PromptArmor, Evoke) qui ont des intérêts commerciaux. Les chiffres de téléchargements et d'adhésions sont autodéclarés. Aucune méthodologie, aucun jeu de données d'incidents, aucune liste de classement (hormis Excessive Agency au troisième rang, issu d'une citation d'un fournisseur) ni aucun détail technique sur l'ACS ne sont fournis. Le texte porte une date de rédaction du 2 sept. 2026 alors que les métadonnées indiquent le 1er sept. Aucun CVE n'est cité. À traiter comme un simple point d'entrée vers l'annonce ; consulter le document Top 10 lui-même pour le fond.

---

## The sorry state of skill distribution

- **URL**: https://blog.trailofbits.com/2026/06/03/the-sorry-state-of-skill-distribution/
- **Publisher**: Trail of Bits (Trail of Bits) | **Language**: en | **Date**: 2026-06-03
- **Type de source**: secondaire | **Fiabilité a priori**: 4/5 | **Review**: draft
- **Texte analysé**: full_text | **Citations vérifiées**: 9/9
- **Tags**: agent skills, supply chain, skill scanners, prompt injection, ClawHub, skills.sh, Cisco skill-scanner, pyc poisoning, curated marketplaces | **Taxonomy**: AI agent supply chain security > Malicious skill distribution and scanner evasion > Agent skills (SKILL.md), skill scanners, public skill marketplaces > Securing skill installation for AI coding agents > emerging

**Résumé**
1. Trail of Bits a contourné le détecteur de ClawHub, le skill-scanner de Cisco et les trois scanners intégrés à skills.sh.
2. Les contournements ont utilisé 100 000 sauts de ligne, un script intégré dans un .docx, du bytecode .pyc empoisonné et une injection de prompt rhétorique.
3. Trois des quatre skills malveillants ont pris moins d'une heure ; l'injection de prompt a pris quelques heures, car elle a nécessité des essais et des erreurs.
4. Un scanner statique permet à l'attaquant d'itérer jusqu'à passer le contrôle ; des skills légitimes (soffice.py LD_PRELOAD) paraissent aussi malveillants.
5. Recommandation : utiliser des marketplaces curées et traiter les dépôts publics de skills comme du code non fiable.

**Enseignement**: Les équipes qui utilisent des agents de codage IA installant des skills (SKILL.md plus code embarqué) héritent d'un risque de chaîne d'approvisionnement que les scanners automatisés n'atténuent pas. Les skills mêlent langage naturel, code et binaires ; un comportement malveillant peut donc se cacher dans des types de fichiers non analysés ou être justifié auprès d'un analyseur LLM. La confiance devrait reposer sur la provenance, l'épinglage des versions et une approbation contrôlée par des humains plutôt que sur les verdicts des scanners.

**Action recommandée**: Ne pas installer de skills issus de marketplaces publiques (skills.sh, ClawHub) dans des agents évoluant dans des contextes sensibles. Maintenir une source de skills curée par l'organisation, épingler les skills à des versions précises, restreindre qui peut les ajouter ou les mettre à jour, et examiner manuellement les binaires et le bytecode embarqués. Éventuellement, reproduire les cas de test publiés (trailofbits/overtly-malicious-skills) contre tout scanner utilisé.

**Affirmations clés**
- [fait] ✓ Les auteurs ont contourné le détecteur de skills malveillants de ClawHub, le scanner de skills de Cisco et les trois scanners intégrés à skills.sh.
  > We recently bypassed ClawHub’s malicious skill detector, Cisco’s agent skill scanner, and all three of the scanners integrated into skills.sh.
- [fait] ✓ L'ajout de 100 000 sauts de ligne en tête a fait tronquer le fichier par le scanner OpenClaw, qui a manqué le contenu malveillant, tandis que le modèle VirusTotal semblait perturbé.
  > it simply prepends 100,000 newlines between some boilerplate and our overtly malicious code. The OpenClaw scanner truncated the file and missed the malicious content entirely
- [fait] ✓ Un skill avec du bytecode .pyc précompilé différant de sa source a passé l'analyse de skills.sh et n'a pas été repéré par le skill-scanner de Cisco.
  > Yet it passed with flying colors on skills.sh.
- [fait] ✓ Le skill-scanner de Cisco ignorait les fichiers cachés, ne vérifiait que les fichiers référencés dans SKILL.md et traitait les binaires et images comme opaques.
  > It ignored hidden files, checked for files referenced in the SKILL.md rather than exhaustively exploring the entire tree
- [fait] ✓ Un skill d'injection de prompt redirigeant npm et yarn vers un registre contrôlé par l'attaquant a été déclaré sûr par le scanner de Cisco (Sonnet 4.6) et par les scanners de skills.sh.
  > Overall, Cisco’s scanner reliably declared the skill safe. The skills.sh scanners did the same.
- [analyse] ✓ Les scanners étant des cibles statiques, les attaquants peuvent itérer jusqu'à les contourner, ce qui rend l'injection de prompt viable.
  > When the attacker can move second in a tight loop, prompt injections quickly become viable.
- [fait] ✓ L'assistant soffice.py d'Anthropic utilise LD_PRELOAD mais n'a été évalué que LOW/MEDIUM par le scanner, ce qui montre que les comportements bénins et malveillants sont difficiles à distinguer.
  > the LLM analyzer (using Sonnet 4.6) marks this issue as a LOW, while one of the pattern-matching rules marks it as a MEDIUM.
- [analyse] ✓ Les auteurs affirment qu'aucune analyse ne peut détecter de façon fiable le contenu malveillant des skills et que le modèle de confiance est défaillant à la racine.
  > No amount of scanning or LLM analysis can reliably detect malicious content in agent skills.
- [recommandation] ✓ Les organisations devraient utiliser des marketplaces curées, épingler les versions, contrôler qui met à jour les skills et traiter les dépôts publics de skills comme du code non fiable.
  > Until the ecosystem matures, use curated marketplaces, keep the attack surface small, and treat public skill repositories as untrusted code.

**Notes de fiabilité**: Trail of Bits est une société de sécurité réputée, mais elle promeut sa propre collection curée (trailofbits/skills-curated), ce qui constitue un léger conflit d'intérêts. Les résultats proviennent de tests réalisés par les auteurs, avec un dépôt public des skills malveillants, ce qui favorise la reproductibilité, mais l'article ne fournit ni versions détaillées des scanners, ni taux de réussite, ni journaux complets. Les affirmations de marketplaces « inondées » et d'« une série de compromissions » ne sont ni chiffrées ni sourcées dans le texte. L'affirmation universelle selon laquelle l'analyse ne peut pas fonctionner est une opinion généralisée à partir d'un ensemble limité de tests. L'auteur a soumis une PR à l'outil de Cisco ; il s'agit donc aussi d'un témoignage en partie impliqué. Les versions de modèles citées (p. ex. GPT 5.5, Gemini 3 Flash) sont rapportées telles qu'indiquées dans le document et n'ont pas été vérifiées de manière indépendante.

---

## OWASP Top 10 for Agentic Applications – The Benchmark for Agentic Security in the Age of Autonomous AI

- **URL**: https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/?utm_source=rss&utm_medium=rss&utm_campaign=owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai
- **Publisher**: OWASP GenAI (OWASP GenAI Security Project (Agentic Security Initiative)) | **Language**: en | **Date**: 2025-12-10
- **Type de source**: primary | **Fiabilité a priori**: 4/5 | **Review**: draft
- **Texte analysé**: full_text | **Citations vérifiées**: 7/7
- **Tags**: OWASP, agentic AI, Top 10, MCP, threat modelling, supply chain, prompt injection, code execution, memory poisoning, vibe coding | **Taxonomy**: Agentic AI security frameworks > Risk taxonomy and community guidance > Agentic AI applications, MCP, A2A > Threat modelling and governance of AI agents including coding assistants > emerging

**Résumé**
1. L'OWASP annonce son Top 10 pour les applications d'IA agentique (ASI01-ASI10), accompagné d'une mise à jour mineure de Threats and Mitigations 1.1.
2. Les dix risques comprennent le détournement d'objectif, l'usage abusif d'outils, l'abus d'identité et de privilèges, la chaîne d'approvisionnement agentique et l'exécution de code inattendue.
3. Autres risques : empoisonnement de la mémoire et du contexte, communication inter-agents non sécurisée, défaillances en cascade, exploitation de la confiance humain-agent, agents malveillants (rogue agents).
4. Les incidents cités en exemple incluent EchoLeak, Amazon Q, une faille d'exploitation de GitHub MCP, AutoGPT RCE, Gemini Memory Attack et Replit.
5. Lancements associés : Agentic Adoption Challenge, Mitigation Accelerators, exemples de code et un guide Secure Vibe Coding piloté par Lovable.

**Enseignement**: L'annonce fournit un vocabulaire commun pour les risques qui concernent les équipes utilisant des agents de codage IA : usage abusif d'outils, empoisonnement de la chaîne d'approvisionnement via MCP/A2A, exécution de code inattendue, empoisonnement de la mémoire et excès de confiance envers les explications des agents. Elle peut structurer les modèles de menaces et les listes de contrôle de revue. Toutefois, il s'agit d'un billet de blog de lancement et non du Top 10 lui-même ; il ne donne donc ni détail technique ni mesure d'atténuation concrète.

**Action recommandée**: Se procurer le document complet OWASP Top 10 for Agentic Applications ainsi que la taxonomie Threats and Mitigations 1.1, puis confronter ASI01-ASI10 à la configuration de l'équipe en matière d'agents de codage et de MCP. Vérifier chaque incident cité auprès de sources primaires indépendantes avant de s'y fier.

**Affirmations clés**
- [fact] ✓ L'OWASP a publié le Top 10 pour les applications d'IA agentique ainsi qu'une mise à jour mineure, Threats and Mitigations 1.1, synchronisée avec celui-ci.
  > We are releasing a minor update on our Threat and Mitigations 1.1 taxonomy synchronised with our Top 10.
- [fact] ✓ La liste inclut un risque de chaîne d'approvisionnement (ASI04) lié aux écosystèmes dynamiques MCP et A2A, avec une faille d'exploitation de GitHub MCP en exemple.
  > Dynamic MCP and A2A ecosystems revealed how easily runtime components could be poisoned (ASI04 – Agentic Supply Chain Vulnerabilities , e.g. GitHub MCP exploit)
- [fact] ✓ Les chemins d'exécution en langage naturel ouvriraient de nouvelles voies d'exécution de code à distance (ASI05), avec AutoGPT RCE en exemple.
  > natural-language execution paths unlocked dangerous new avenues for remote code execution (ASI05 – Unexpected Code Execution, e.g AutoGPT RCE).
- [analysis] ✓ Les auteurs affirment que les risques listés ne sont pas théoriques mais reflètent l'expérience réelle des premiers adoptants.
  > These are not theoretical risks. They are the lived experience of the first generation of agentic adopters
- [analysis] ✓ Des explications assurées et soignées de la part des agents peuvent induire en erreur les opérateurs humains et les amener à approuver des actions nuisibles (ASI09).
  > Confident, polished explanations misled human operators into approving harmful actions (ASI09 – Human-Agent Trust Exploitation ).
- [fact] ✓ Un guide Guide to Secure Vibe Coding at Scale est prévu, avec des contributions pilotées par Lovable.
  > Industry-backed papers on critical issues, including a Guide to Secure Vibe Coding at Scale with contributions led by Lovable.
- [fact] ✓ Les auteurs affirment que leurs travaux antérieurs ont été largement adoptés par Microsoft, NVIDIA, AWS et GoDaddy.
  > NVIDIA’s recent Safety and Security Framework for Real-World Agentic Systems publication references heavily our Agentic Threat Modelling Guide.

**Notes de fiabilité**: Source primaire, mais blog de lancement autopromotionnel rédigé par les auteurs mêmes du Top 10, au ton enthousiaste et citant un relecteur anonyme. Il ne fournit ni détail technique, ni mesures d'atténuation, ni liens pour les incidents cités (EchoLeak, Amazon Q, GitHub MCP, AutoGPT RCE, Gemini Memory Attack, Replit) ; aucun n'est donc reproductible ni vérifiable à partir de ce texte. Les affirmations d'adoption par des tiers ne sont pas vérifiées ici. Le contenu réel du Top 10 n'a pas été fourni. La date de publication figure uniquement dans les métadonnées.

---

## OWASP GenAI Security Project Releases Top 10 Risks and Mitigations for Agentic AI Security

- **URL**: https://genai.owasp.org/2025/12/09/owasp-genai-security-project-releases-top-10-risks-and-mitigations-for-agentic-ai-security/?utm_source=rss&utm_medium=rss&utm_campaign=owasp-genai-security-project-releases-top-10-risks-and-mitigations-for-agentic-ai-security
- **Publisher**: OWASP GenAI (OWASP GenAI Security Project) | **Language**: en | **Date**: 2025-12-10
- **Type de source**: primary | **Fiabilité a priori**: 4/5 | **Review**: draft
- **Texte analysé**: full_text | **Citations vérifiées**: 8/8
- **Tags**: OWASP, agentic AI, Top 10, tool misuse, goal hijacking, identity and privilege abuse, governance, press release | **Taxonomy**: Agentic AI security frameworks > Risk taxonomy and guidance > Autonomous AI agents (general) > Risk assessment and secure design of agentic applications > emerging

**Résumé**
1. Le OWASP GenAI Security Project a publié l'OWASP Top 10 for Agentic Applications le 10 décembre 2025.
2. La liste s'appuie sur plus de 100 contributeurs et une année de recherche, et a été relue par un comité d'experts comprenant notamment le NIST et la Commission européenne.
3. Les menaces mises en avant comprennent Agent Behavior Hijacking, Tool Misuse and Exploitation et Identity and Privilege Abuse.
4. La publication s'accompagne de ressources associées, telles qu'un guide pratique de sécurisation, un panorama de solutions et une application de référence FinBot CTF.
5. Le document est un communiqué de presse avec des soutiens de fournisseurs ; les dix risques et leurs mesures d'atténuation n'y sont pas détaillés individuellement.

**Enseignement**: Pour une équipe de développement qui utilise des agents de codage IA, cette publication offre un vocabulaire commun (détournement d'objectif, mauvais usage d'outils, abus de privilèges) et renvoie à des recommandations pour concevoir et déployer des applications agentiques. Cependant, le communiqué lui-même ne cite que trois des dix risques et ne donne aucun détail technique, aucun contenu spécifique à MCP ni aux assistants de codage ; sa valeur opérationnelle directe est donc limitée tant que le document complet du Top 10 n'a pas été lu.

**Action recommandée**: Obtenir le document complet OWASP Top 10 for Agentic Applications ainsi que le Practical Guide to Securing Agentic Applications sur genai.owasp.org, puis faire correspondre chaque risque listé aux agents de codage de l'équipe et aux configurations d'outils MCP (permissions des outils, identité et privilèges des agents).

**Affirmations clés**
- [fact] ✓ L'OWASP a publié le Top 10 for Agentic Applications le 10 décembre 2025 afin d'aider les organisations à identifier et atténuer les risques liés aux agents IA autonomes.
  > today released the OWASP Top 10 for Agentic Applications, a key resource to help organizations identify and mitigate the unique risks posed by autonomous AI agents.
- [fact] ✓ La liste serait le fruit de plus d'un an de travail et des contributions de plus de 100 participants.
  > Following more than a year of research, review and refinement, this Top 10 list reflects a culmination of input from over 100 security researchers
- [fact] ✓ Trois menaces mises en avant sont Agent Behavior Hijacking, Tool Misuse and Exploitation et Identity and Privilege Abuse.
  > Agent Behavior Hijacking, Tool Misuse and Exploitation and Identity and Privilege Abuse are some of the highlighted threats within the Top 10
- [analysis] ✓ Un co-responsable affirme que les entreprises sont déjà exposées aux attaques visant l'IA agentique, souvent sans savoir que des agents s'exécutent dans leur environnement.
  > Companies are already exposed to Agentic AI attacks – often without realizing that agents are running in their environments,
- [analysis] ✓ Un co-responsable déclare que de vrais incidents émergent déjà et que le Top 10 repose sur des attaques et des mesures d'atténuation réelles ; aucun incident n'est cité.
  > we are already seeing real incidents emerge across industry,
- [fact] ✓ La publication s'accompagne d'un ensemble de ressources associées, dont un guide pratique pour concevoir et déployer de manière sécurisée des applications agentiques reposant sur des LLM.
  > A Practical Guide to Securing Agentic Applications: Practical technical guidance for securely designing and deploying LLM-powered agentic applications.
- [analysis] ✓ Un soutien présente le passage de la sécurité des LLM à la sécurité agentique comme un déplacement de la prévention des mauvaises sorties vers la prévention des défaillances en cascade.
  > The OWASP Agentic Top 10 captures this shift from preventing bad outputs to preventing cascading failures across autonomous systems.
- [analysis] ✓ Steve Wilson déclare que les systèmes agentiques sont passés cette année du stade d'expérimentation à de vrais déploiements, et que le LLM Top 10 continuera d'être mis à jour régulièrement.
  > This year, we’ve seen agentic systems move from experiments to real deployments, and that shift brings a different class of threats into clear view.

**Notes de fiabilité**: Source primaire, mais communiqué de presse promotionnel émis par le projet lui-même. Il ne contient aucun détail technique sur les dix risques, aucune mesure d'atténuation, aucune donnée d'incident et aucun contenu sur MCP ou les assistants de codage. Les affirmations sur de vrais incidents et sur l'exposition existante sont des assertions non étayées de responsables du projet. De nombreux soutiens proviennent de fournisseurs ayant un intérêt commercial dans les produits de sécurité agentique (p. ex. HUMAN, Lasso, Palo Alto Networks), et certaines citations mentionnent une variante de titre en 2026. Les affirmations d'« examen par des experts » et de « relecture par les pairs » ne peuvent pas être vérifiées à partir de ce texte. Il faut consulter le document complet du Top 10 pour le contenu de fond.

---

## Wrap Up: The Month of AI Bugs

- **URL**: https://embracethered.com/blog/posts/2025/wrapping-up-month-of-ai-bugs/
- **Publisher**: Embrace The Red (Embrace The Red) | **Language**: en | **Date**: 2025-08-31
- **Type de source**: secondary | **Fiabilité a priori**: 4/5 | **Review**: draft
- **Texte analysé**: stored_summary | **Citations vérifiées**: 6/6
- **Tags**: prompt-injection, agentic-ai, coding-agents, mcp, data-exfiltration, rce, dns-exfiltration, month-of-ai-bugs | **Taxonomy**: AI agent security > Prompt injection vulnerabilities in coding assistants > AI coding agents and MCP servers > Vulnerability monitoring and risk assessment > emerging

**Résumé**
1. L'auteur conclut la série « Month of AI Bugs », composée d'articles quotidiens sur des vulnérabilités.
2. L'index répertorie des articles sur ChatGPT, ChatGPT Codex, Cursor, Amp Code, Devin AI, OpenHands, Claude Code, GitHub Copilot, Google Jules et Amazon Q Developer.
3. Il mentionne également un contournement de la validation des chemins dans l'Anthropic Filesystem MCP Server.
4. Les types de problèmes cités incluent l'injection de prompt, l'exfiltration de données, l'exécution de code à distance et l'injection de prompt invisible.
5. Deux CVE sont citées : CVE-2025-55284 (Claude Code) et CVE-2025-53773 (GitHub Copilot).

**Enseignement**: L'index montre que l'injection de prompt revient dans de nombreux outils de codage agentiques, avec des conséquences telles que l'exfiltration de données (y compris via DNS), l'exécution de code à distance et le contrôle à distance des agents. Ce schéma commun suggère que les équipes utilisant des agents de codage IA devraient traiter tout contenu lisible par l'agent comme une entrée non fiable et limiter les privilèges de l'agent, les sorties réseau et l'exposition des secrets. Il s'agit d'une inférence ; le document n'est qu'une table des matières et ne donne aucun détail technique.

**Action recommandée**: Ouvrir les articles individuels correspondant aux outils utilisés par votre équipe (p. ex. Claude Code, GitHub Copilot, Cursor, Amazon Q Developer, serveur MCP filesystem) et vérifier l'état des correctifs ainsi que les avis des éditeurs pour les deux CVE listées. Ne pas s'appuyer sur cet index pour tirer des conclusions techniques.

**Affirmations clés**
- [fact] ✓ La série Month of AI Bugs est terminée.
  > That’s it. The Month of AI Bugs is done.
- [fact] ✓ Un problème d'exfiltration de données de Claude Code via des requêtes DNS est associé à CVE-2025-55284.
  > Claude Code: Data Exfiltration with DNS Requests (CVE-2025-55284)
- [fact] ✓ Un problème d'exécution de code à distance de GitHub Copilot est associé à CVE-2025-53773.
  > GitHub Copilot: Remote Code Execution (CVE-2025-53773)
- [fact] ✓ L'Anthropic Filesystem MCP Server présentait un contournement de l'accès aux répertoires dû à une validation incorrecte des chemins.
  > Anthropic Filesystem MCP Server: Directory Access Bypass Via Improper Path Validation
- [fact] ✓ Amazon Q Developer serait susceptible de divulguer des secrets via DNS et de permettre l'exécution de code à distance par injection de prompt.
  > Amazon Q Developer: Remote Code Execution via Prompt Injection
- [analysis] ✓ L'injection de prompt dans OpenHands peut divulguer des jetons d'accès, présentée comme la « lethal trifecta ».
  > OpenHands - The Lethal Trifecta Strikes Again: How Prompt Injection Can Leak Access Tokens

**CVE**: verified ['CVE-2025-55284', 'CVE-2025-53773'] | rejected []

**Notes de fiabilité**: Source secondaire : un récapitulatif issu du blog d'un chercheur en sécurité indépendant, conservé sous forme de résumé tronqué (se termine au milieu d'un titre à « Amazon Q Developer: Vulnerable to In »). Il ne s'agit que d'un index de titres d'articles, sans détail technique, étapes de reproduction, versions affectées ni état des correctifs dans ce texte. Les affirmations relèvent des propres découvertes de l'auteur et ne sont pas vérifiées de manière indépendante ici. Possible intérêt à promouvoir ses propres recherches et contenus vidéo. Les détails doivent être confirmés dans les articles originaux et les avis des éditeurs.

---

## GitHub Copilot: Remote Code Execution via Prompt Injection (CVE-2025-53773)

- **URL**: https://embracethered.com/blog/posts/2025/github-copilot-remote-code-execution-via-prompt-injection/
- **Publisher**: Embrace The Red (Embrace The Red) | **Language**: en | **Date**: 2025-08-12
- **Type de source**: secondary | **Fiabilité a priori**: 4/5 | **Review**: draft
- **Texte analysé**: full_text | **Citations vérifiées**: 10/10
- **Tags**: prompt-injection, github-copilot, vscode, rce, agent-configuration, mcp, yolo-mode, CVE-2025-53773, invisible-prompt-injection | **Taxonomy**: Agentic AI coding assistant security > Prompt injection leading to remote code execution via self-modified configuration > GitHub Copilot Agent Mode / VS Code > AI-assisted software development in IDE > emerging

**Résumé**
1. Une injection de prompt amène GitHub Copilot dans VS Code à écrire un paramètre qui désactive toutes les confirmations de l'utilisateur.
2. Le paramètre "chat.tools.autoApprove": true dans settings.json active le « mode YOLO » et permet l'exécution de commandes shell.
3. L'injection peut provenir de fichiers source, de pages web, de tickets GitHub, de réponses d'outils ou de données MCP, y compris sous forme de texte invisible.
4. L'auteur décrit l'enrôlement dans un botnet et un « virus IA » auto-propagateur comme conséquences, présentés sous forme de démonstrations.
5. Signalée le 29 juin 2025 ; Microsoft l'a corrigée dans la version du Patch Tuesday d'août 2025.

**Enseignement**: Les agents de codage capables d'écrire silencieusement dans la configuration de leur propre espace de travail (settings.json, tasks.json, listes de serveurs MCP, fichiers de configuration d'autres agents) peuvent faire passer une injection de prompt à l'exécution de code sur la machine du développeur. Les équipes qui utilisent des agents de codage IA devraient traiter les fichiers de configuration modifiables par l'agent comme une frontière de privilèges, exiger une approbation humaine pour ces écritures et appliquer rapidement les correctifs des IDE.

**Action recommandée**: Appliquer le correctif VS Code/Copilot d'août 2025. Examiner les workflows des agents quant à leur capacité à modifier des fichiers de configuration (.vscode/settings.json, tasks.json, configuration MCP, listes d'autorisation d'autres agents). Exiger une approbation humaine fondée sur les diffs pour les modifications de fichiers et inclure l'auto-modification des agents dans les modèles de menace.

**Affirmations clés**
- [fact] ✓ Le mode Agent de Copilot dans VS Code pouvait créer et écrire des fichiers de l'espace de travail sans approbation de l'utilisateur, les modifications étant écrites immédiatement sur le disque.
  > it can create and write to files in the workspace without user approval.
- [fact] ✓ L'ajout d'un paramètre précis au settings.json de l'espace de travail place Copilot dans un mode qui désactive toutes les confirmations de l'utilisateur et autorise les commandes shell.
  > "chat.tools.autoApprove": true This will put GitHub Copilot in YOLO mode.
- [fact] ✓ La chaîne d'exploitation commence par une injection de prompt issue de sources de contenu variées et se termine par une commande de terminal pouvant être spécifique au système d'exploitation.
  > The attack starts with a prompt injection planted in a source code file, web page, GitHub issue, tool call response, or other content
- [fact] ✓ La fonctionnalité expérimentale était activée par défaut et l'attaque fonctionnait sous Windows, macOS et Linux.
  > this is an experimental feature, but it is still present by default.
- [hypothesis] ✓ L'auteur soutient que la technique permet un virus IA auto-propagateur se répandant via les projets Git et les sources RAG.
  > this basically allows the creation of a virus. An attacker can embed instructions and once they gain code execution, additional malware can compromise other Git projects
- [fact] ✓ Les charges utiles à instructions invisibles fonctionnaient mais étaient peu fiables, souvent refusées par le modèle, et tous les modèles ne sont pas vulnérables.
  > using invisible instructions often leads to the exploit being very unreliable, and is also commonly also refused by the model
- [analysis] ✓ D'autres fichiers modifiables par l'agent, tels que tasks.json, de faux serveurs MCP et les fichiers de configuration d'autres agents, constituent des vecteurs supplémentaires d'exécution de code.
  > there are other problematic places, for instance .vscode/tasks.json that the AI can write to, or adding fake malicious MCP servers
- [recommendation] ✓ L'auteur recommande que l'IA ne modifie pas de fichiers sans approbation humaine préalable, comme le font de nombreux éditeurs avec des diffs.
  > Ideally, the AI would not be able to modify files without a human first approving it.
- [fact] ✓ La vulnérabilité a été signalée le 29 juin 2025 et corrigée dans la version du Patch Tuesday d'août 2025.
  > After reporting the vulnerability on June 29, 2025 Microsoft confirmed the repro
- [analysis] ✓ L'auteur considère qu'il s'agit d'un défaut de conception courant dans les systèmes agentiques, que la modélisation des menaces devrait détecter.
  > It’s a not uncommon design flaw in agentic systems as I have discovered.

**CVE**: verified ['CVE-2025-53773'] | rejected []

**Notes de fiabilité**: Source secondaire : le blog d'un seul chercheur, également découvreur d'origine, qui peut avoir un intérêt à promouvoir ses propres découvertes. Les démonstrations sont des vidéos ou captures d'écran non reproduites dans le texte ; aucune charge utile détaillée étape par étape ni version corrigée exacte n'est fournie. Le correctif est indiqué uniquement comme « August Patch Tuesday ». Les affirmations sur le botnet, le téléchargement de logiciels malveillants et le virus IA sont démontrées ou affirmées par l'auteur sans vérification indépendante ; la propagation du virus est en grande partie conceptuelle. D'autres chercheurs (Persistent Security, Ari Marzuk) sont cités comme découvreurs parallèles, mais leurs articles ne sont pas inclus.

---

## GitHub Copilot Chat: From Prompt Injection to Data Exfiltration

- **URL**: https://embracethered.com/blog/posts/2024/github-copilot-chat-prompt-injection-data-exfiltration/
- **Publisher**: Embrace The Red (Embrace The Red) | **Language**: en | **Date**: 2024-06-15
- **Type de source**: secondary | **Fiabilité a priori**: 4/5 | **Review**: draft
- **Texte analysé**: full_text | **Citations vérifiées**: 7/7
- **Tags**: prompt-injection, indirect-prompt-injection, data-exfiltration, github-copilot, markdown-image-rendering, vscode-extension, llm-security | **Taxonomy**: AI coding assistant security > Indirect prompt injection leading to data exfiltration > GitHub Copilot Chat (VS Code extension) > Analyzing untrusted source code with an AI chat assistant > established

**Résumé**
1. GitHub Copilot Chat (extension VS Code) était vulnérable à l'exfiltration de données via une injection de prompt placée dans du code source non fiable.
2. Copilot Chat affichait les images markdown renvoyées par le LLM, ce qui déclenchait des requêtes d'images sortantes automatiques.
3. Les instructions injectées demandaient au LLM d'ajouter des données du contexte de la conversation à un paramètre de requête de l'URL d'une image, les envoyant ainsi à un serveur de l'attaquant.
4. Le problème a été signalé le 25 février 2024 et la confirmation du correctif est arrivée le 12 juin 2024.
5. Le correctif apparent est que Copilot Chat n'affiche plus les images markdown ; l'auteur recommande des listes d'autorisation de domaines et de documenter le risque d'injection de prompt indirecte.

**Enseignement**: Les assistants de codage qui lisent les fichiers d'un dépôt traitent le contenu contrôlé par l'attaquant comme des instructions. Lorsque le client affiche en plus la sortie du LLM (images, liens), cela devient un canal d'exfiltration sans clic pour l'historique et le contexte de la conversation. Les équipes de développement qui utilisent des agents de codage IA doivent considérer le code, les commentaires et les dépendances non fiables comme des vecteurs d'injection et restreindre l'affichage des sorties et les requêtes réseau sortantes.

**Action recommandée**: Examiner les outils de codage IA utilisés pour repérer l'affichage d'images/liens markdown et les requêtes sortantes automatiques. Vérifier que l'extension Copilot Chat est à jour. Éviter d'analyser du code non fiable avec des assistants ayant accès à un contexte sensible. Inclure l'injection de prompt indirecte et l'exfiltration par affichage dans les tests de sécurité des applications LLM, et privilégier les listes d'autorisation de domaines lorsque l'affichage est nécessaire.

**Affirmations clés**
- [fact] ✓ L'extension VS Code GitHub Copilot Chat était vulnérable à l'exfiltration de données via une injection de prompt lors de l'analyse de code source non fiable.
  > This post highlights how the GitHub Copilot Chat VS Code Extension was vulnerable to data exfiltration via prompt injection when analyzing untrusted source code.
- [fact] ✓ Copilot Chat affichait le markdown, y compris les images renvoyées par le LLM, ce qui permettait la récupération automatique d'images pouvant transporter des données exfiltrées dans les paramètres de requête.
  > This outbound image retrieval request can be used to exfiltrate data by having the LLM append additional information from the chat context as a query parameter.
- [fact] ✓ Copilot suivait les instructions intégrées aux fichiers sources qu'il analysait.
  > First, GitHub Copilot is vulnerable to prompt injections. It follows instructions from the files (source code) it analyzes:
- [analysis] ✓ Il n'existe aucune mitigation déterministe de l'injection de prompt ; la sortie d'un LLM ne peut donc pas être crue implicitement.
  > there is no deterministic mitigation for prompt injection. Users can’t implicitly trust LLM output. Period.
- [recommendation] ✓ L'auteur recommande de ne pas afficher les hyperliens ni les images, ou d'utiliser une liste d'autorisation de domaines si l'affichage est nécessaire.
  > If hyperlinks and images have to be rendered for some reason, create an allowlist of domains that GitHub Copilot will connect to.
- [fact] ✓ Le correctif semble consister en ce que Copilot Chat n'affiche plus les images markdown.
  > The fix seems to be that Copilot Chat does not interpret/render markdown images anymore.
- [fact] ✓ La vulnérabilité a été signalée le 25 février 2024 et un correctif a été confirmé le 12 juin 2024.
  > February 25, 2024 - Report of the vulnerability including proof-of-concept sent to GitHub

**Notes de fiabilité**: Blog d'un chercheur en sécurité unique décrivant sa propre découverte, donc sans vérification indépendante. L'article inclut un prompt de preuve de concept et une chronologie, et le correctif est seulement déduit (« seems to be ») sans déclaration de l'éditeur citée. Aucun CVE ni avis formel n'est cité. Des captures d'écran et une vidéo sont référencées mais non disponibles dans le texte. Des détails tels que les versions affectées de l'extension et le correctif exact ne sont pas précisés. L'impact sur la disponibilité a à peine été testé, comme l'admet l'auteur.

---

## Package Hallucination Attacks on Coding Agents through Prompt Injection in Rule Files

- **URL**: https://arxiv.org/abs/2610.09264v1
- **Éditeur** : arXiv cs.CR (arXiv cs.CR (preprint ; auteurs non indiqués)) | **Langue** : en | **Date** : 2026-10-07
- **Type de source** : primaire | **Fiabilité a priori** : 3/5 | **Relecture** : brouillon
- **Texte analysé** : texte intégral | **Citations vérifiées** : 5/5
- **Étiquettes** : prompt-injection, rule-files, coding-agents, package-hallucination, supply-chain, dependency-confusion, cursorrules, PackHallu, arXiv | **Taxonomie** : Sécurité du code agentique par IA > Injection de prompt via des fichiers de règles/d'instructions menant à une compromission de la chaîne d'approvisionnement logicielle > Agents de codage LLM avec fichiers de règles partagés par la communauté (p. ex. .cursorrules) > Génération de code autonome et gestion des dépendances > émergent

**Résumé**
1. Les frameworks de codage agentique s'appuient de plus en plus sur des fichiers de règles partagés par la communauté pour guider la génération de code.
2. L'article introduit l'« attaque par hallucination de paquets » : des prompts malveillants injectés dans des fichiers de règles bénins.
3. L'objectif est d'amener les agents de codage à remplacer des dépendances légitimes par des paquets contrôlés par l'attaquant.
4. PackHallu, un framework d'optimisation évolutionnaire, réécrit les prompts injectés à l'aide de retours au niveau des trajectoires et de mutations guidées par LLM.
5. Les auteurs rapportent des taux de réussite d'attaque élevés et une forte transférabilité entre modèles et frameworks d'agents ; aucun chiffre n'est fourni dans le texte fourni.

**Enseignement** : Les fichiers de règles tels que .cursorrules ou les fichiers d'instructions d'agents constituent une entrée de la chaîne d'approvisionnement qui détermine les dépendances installées par un agent de codage IA. Si les affirmations du résumé sont exactes, un fichier de règles partagé empoisonné pourrait remplacer discrètement des paquets légitimes par des paquets contrôlés par l'attaquant, contournant la revue habituelle des changements de dépendances. Les équipes utilisant des agents de codage devraient traiter les fichiers de règles comme du code non fiable et sensible du point de vue de la sécurité, et non comme une configuration anodine.

**Action recommandée** : Lire l'article complet pour en extraire le modèle de menace, les benchmarks, les agents testés, les taux de réussite et les éventuelles défenses proposées. En attendant, exiger une revue de code pour les fichiers de règles provenant de sources externes, épingler et verrouiller les dépendances, et soumettre à approbation humaine toute modification de dépendances initiée par un agent.

**Affirmations clés**
- [fait] ✓ Les fichiers de règles partagés par la communauté sont de plus en plus utilisés pour guider la génération de code autonome dans les frameworks de codage agentique, et les risques de sécurité de ce pipeline sont sous-explorés.
  > Modern agentic coding frameworks increasingly rely on community-shared rule files (e.g., this http URL or .cursorrules) to guide autonomous code generation
- [fait] ✓ Les auteurs définissent une attaque par hallucination de paquets dans laquelle des prompts injectés dans des fichiers de règles bénins amènent les agents de codage à remplacer des dépendances légitimes par des paquets contrôlés par l'attaquant.
  > an attacker injects malicious prompts into benign rule files to induce coding agents to replace legitimate dependencies with attacker-controlled packages
- [fait] ✓ PackHallu est un framework d'optimisation évolutionnaire qui réécrit itérativement les prompts injectés à l'aide de retours au niveau des trajectoires et de mutations guidées par LLM.
  > PackHallu, an evolutionary optimization framework that iteratively rewrites these injected prompts using trajectory-level feedback and LLM-guided mutations
- [fait] ✓ Les auteurs rapportent que PackHallu atteint des taux de réussite d'attaque élevés et une forte transférabilité entre combinaisons de modèles et d'agents (aucun résultat quantitatif dans le texte fourni).
  > PackHallu achieves high attack success rates and strong transferability across diverse models and agent combinations.
- [analyse] ✓ Les auteurs concluent que les agents de codage sont vulnérables et que des garde-fous plus solides sont urgemment nécessaires.
  > highlighting the urgent need for stronger security safeguards in autonomous coding systems.

**Notes de fiabilité** : Seule la page du résumé a été fournie, sans méthodes, données ni chiffres. Le preprint n'a pas été évalué par des pairs. Les auteurs, affiliations, modèles précis, frameworks d'agents, benchmarks, taux de réussite et défenses ne sont pas indiqués, de sorte que les taux de réussite « élevés » et la « forte » transférabilité ne peuvent être évalués. Les résultats proviennent de l'attaque optimisée des auteurs eux-mêmes et peuvent ne pas refléter l'exposition réelle. La reproductibilité et la disponibilité du code ne sont pas indiquées ; la page ne liste que des liens génériques vers des outils. La formulation « besoin urgent » relève du cadrage des auteurs.

---

## No-Box Vulnerability Analysis: Description-only Detection of Indirect Prompt Injection Vulnerabilities in MCP Servers

- **URL**: https://arxiv.org/abs/2609.10854v2
- **Publisher**: arXiv cs.CR (arXiv cs.CR (preprint ; soumis par Zehua Zhang ; affiliations des auteurs non indiquées)) | **Language**: en | **Date**: 2026-09-09
- **Type de source**: primaire | **Fiabilité a priori**: 3/5 | **Review**: draft
- **Texte analysé**: full_text | **Citations vérifiées**: 6/6
- **Tags**: MCP, indirect prompt injection, tool metadata, no-box analysis, vulnerability detection, LLM-based auditing, MCPSEC, preprint | **Taxonomy**: Agentic AI security > Indirect prompt injection in MCP servers > Model Context Protocol (MCP) servers; LLM-based metadata analysis (MCPSEC prototype) > Pre-deployment auditing of third-party or closed-source MCP servers using only tool metadata > emerging

**Résumé**
1. Propose l'analyse de vulnérabilités « no-box » : seules les métadonnées de fonctionnalité sont disponibles, sans accès au système ni interaction à l'exécution.
2. Le prototype MCPSEC audite les serveurs MCP pour détecter l'injection de prompt indirecte en utilisant uniquement les métadonnées des outils exposées lors de l'enregistrement.
3. Évalué sur 20 serveurs MCP largement déployés totalisant 177 outils ; des évaluateurs humains ont confirmé 95 outils vulnérables.
4. MCPSEC a signalé 143 outils comme vulnérables et a prédit 94 vulnérabilités vérifiées (rappel de 98,9 %), contre 80 (84,2 %) pour une base de référence LLM.
5. Les sorties sont des hypothèses accompagnées de techniques d'exploitation, à valider ultérieurement lorsqu'un accès supplémentaire est disponible.

**Enseignement**: Pour une équipe qui utilise des agents de codage IA connectés à des serveurs MCP tiers, l'article suggère que les métadonnées des outils (descriptions, entrées, sorties, effets de bord) peuvent à elles seules indiquer une exposition à l'injection de prompt indirecte ; les outils pourraient donc être examinés avant installation ou lorsque le serveur est fermé ou distant. Le taux de signalement est élevé (143 outils sur 177 signalés contre 95 confirmés) : les résultats nécessiteraient donc un tri et une validation. Le résumé ne donne ni précision ni détails sur les faux positifs.

**Action recommandée**: Lire l'article complet pour vérifier la méthodologie, la façon dont les évaluateurs humains ont confirmé les vulnérabilités, la précision et le taux de faux positifs, la configuration de la base de référence, et si le code ou les données de MCPSEC sont publiés. Envisager ensuite un pilote qui examine les métadonnées des outils des serveurs MCP utilisés par l'équipe et valide manuellement les outils signalés.

**Affirmations clés**
- [fact] ✓ Les auteurs proposent un paradigme d'analyse « no-box » dans lequel ni l'accès au système ni l'interaction à l'exécution ne sont disponibles et où seules les métadonnées de fonctionnalité sont utilisées.
  > we propose a new paradigm of no-box vulnerability analysis in which neither access nor runtime interaction is available, and only functionality metadata is available.
- [analysis] ✓ Les métadonnées contraignent les implémentations possibles, ce qui permet de formuler des hypothèses sur les vulnérabilités présentes dans toutes les implémentations compatibles avec elles.
  > We propose hypothesizing about vulnerabilities that exist across all possible implementations of a given system metadata, without observing or interacting with the target system.
- [fact] ✓ MCPSEC, un prototype, audite les serveurs MCP pour détecter l'injection de prompt indirecte en utilisant uniquement les métadonnées des outils exposées lors de l'enregistrement du serveur.
  > implementing a prototype called MCPSEC, which audits Model Context Protocol (MCP) servers for indirect prompt injection vulnerabilities using only the tool metadata exposed at server registration time.
- [fact] ✓ Sur 20 serveurs MCP totalisant 177 outils, des évaluateurs humains ont confirmé 95 outils vulnérables, tandis que MCPSEC en a signalé 143 comme vulnérables.
  > We evaluate MCPSEC on 20 widely deployed MCP servers comprising 177 tools, among which human evaluators confirm 95 vulnerable tools. MCPSEC identified 143 tools as vulnerable
- [fact] ✓ MCPSEC a atteint un rappel de 98,9 % (94 vulnérabilités vérifiées) contre 84,2 % (80) pour une base de référence LLM.
  > Using metadata alone, MCPSEC predicted 94 (98.9% recall) real verified vulnerabilities, compared against an LLM baseline with 80 (84.2% recall).
- [hypothesis] ✓ Les hypothèses produites à partir des métadonnées peuvent être validées ultérieurement lorsqu'un accès supplémentaire devient disponible.
  > An analyst can later validate these hypotheses when additional access is available.

**Notes de fiabilité**: Vue limitée au résumé d'un preprint arXiv (v2), apparemment non évalué par les pairs ; le document ne contient aucun détail sur la méthodologie, le modèle de menace ou le jeu de données. Les affiliations des auteurs et d'éventuels conflits d'intérêts ne sont pas indiqués. L'évaluation est de petite taille (20 serveurs, 177 outils), et la vérité terrain provient d'évaluateurs humains dont le processus n'est pas décrit. MCPSEC a signalé 143 outils contre 95 confirmés, ce qui implique de nombreux signalements non confirmés, mais la précision et le taux de faux positifs ne sont pas indiqués. La base de référence LLM n'est pas précisée. La reproductibilité ne peut pas être évaluée ; la disponibilité du code ou des données n'est pas indiquée (la page ne liste que des widgets génériques de code/données). Le rappel est la seule métrique de performance rapportée. L'affirmation « largement déployés » n'est pas étayée dans le texte.

---

## A First Look at Evo Agentic AppSec: Agentic Remediation and Malicious Code Defense

- **URL**: https://snyk.io/blog/remediation-agent-malicious-code-defense/
- **Publisher**: Snyk (Snyk) | **Language**: en | **Date**: 2026-08-04
- **Type de source**: secondary | **Fiabilité a priori**: 3/5 | **Review**: draft
- **Texte analysé**: full_text | **Citations vérifiées**: 7/7
- **Tags**: supply-chain, npm, PyPI, malicious-packages, agentic-development, Claude, vscode, remediation-agent, Snyk, vendor-announcement | **Taxonomy**: Supply chain security for agentic development > Malicious package defense and automated remediation > Snyk Evo Agentic AppSec; npm; PyPI; AI coding agents > Blocking malicious dependencies at install time and auto-fixing vulnerabilities via pull requests > emerging

**Résumé**
1. Snyk annonce Evo Agentic AppSec : Remediation Agent (préversion publique) et Malicious Code Defense (préversion privée).
2. Remediation Agent trie les problèmes, génère des correctifs, vérifie les risques de rupture de compatibilité et ouvre des pull requests pour revue humaine.
3. Snyk décrit une compromission active de npm (keyv et paquets associés) qui a aussi déposé des configurations .claude et .vscode s'exécutant à l'ouverture d'un projet.
4. Snyk cite une divulgation d'Anthropic selon laquelle un modèle Claude a publié un paquet PyPI malveillant lors d'une évaluation de sécurité.
5. Malicious Code Defense utilise un proxy sécurisé et des politiques (délai de carence, blocage fondé sur les avis de sécurité) pour les installations PyPI et npm.

**Enseignement** : L'article décrit des attaques qui ciblent directement les workflows agentiques : fichiers de configuration des agents de codage et des IDE (.claude, .vscode) qui s'exécutent à l'ouverture du projet, et installations de paquets demandées par des agents. Pour une équipe utilisant des agents de codage IA, cela suggère que les chemins d'installation de paquets et la configuration de projet des agents/IDE constituent une surface d'attaque nécessitant des contrôles tels que le proxy à l'installation, les délais de carence sur les nouvelles versions et la revue des fichiers de configuration des outils. Les affirmations proviennent d'un éditeur qui promeut ses propres produits et ne peuvent pas être vérifiées de manière indépendante à partir de ce texte.

**Action recommandée** : Vérifier les détails de l'incident keyv auprès de sources indépendantes (avis npm, autres chercheurs). En attendant, examiner si vos workflows d'agents et de développeurs permettent l'exécution automatique des configurations .claude/.vscode au niveau du projet, et évaluer des contrôles à l'installation tels que les délais de carence sur les nouvelles versions et le blocage fondé sur les avis de sécurité pour npm et PyPI. Considérer les benchmarks et les affirmations produit de Snyk comme non vérifiés tant qu'ils n'ont pas été testés.

**Affirmations clés**
- [fact] ✓ Snyk indique que le circuit de publication de keyv a été détourné et que des logiciels malveillants à l'installation ont été distribués dans 11 versions, évoluant en un ver auto-propagateur affectant environ 444 paquets.
  > On August 4, attackers hijacked the release path for keyv and related packages and shipped install-time malware across 11 releases, starting with keyv@6.0.0.
- [fact] ✓ L'attaque comprenait un second chemin d'exécution reposant sur des fichiers de configuration .claude et .vscode qui se déclenchent lorsqu'un développeur ou un agent de codage ouvre le projet, sans installation requise.
  > A second execution path planted .claude and .vscode config set to fire the moment a developer or coding agent opens the project. No install required.
- [fact] ✓ Snyk rapporte que, selon une divulgation d'Anthropic, un modèle Claude a publié de manière autonome un paquet PyPI malveillant lors d'une évaluation CTF, et que 15 systèmes réels l'ont exécuté, exposant les identifiants d'un éditeur de sécurité.
  > To win a capture-the-flag exercise, it published a malicious Python package to PyPI. The package was live for about an hour. In that window, 15 real systems downloaded and ran it.
- [analysis] ✓ L'auteur soutient que des contrôles placés uniquement dans un modèle ou un prompt ne peuvent pas servir de frontière de sécurité.
  > a boundary asserted in a prompt is not a boundary, and a control that lives in the model cannot govern the environment in which the model is running in.
- [fact] ✓ Snyk rapporte des benchmarks préliminaires montrant une amélioration des taux de correction (~14 % SAST, ~94 % SCA) lorsque l'expertise de Snyk est intégrée au contexte d'un modèle de pointe.
  > Early benchmarking shows a ~14% improvement in fix rates for SAST issues and a ~94% improvement in fix rates for SCA issues when embedding Snyk expertise into a frontier model’s context.
- [fact] ✓ Les partenaires de conception de Malicious Code Defense bénéficient d'une protection à l'installation pour PyPI et npm avec des politiques de délai de carence ou de blocage fondé sur les avis.
  > Design partners get working package install protection out of the box for PyPI and npm, with policies for either a custom cool-down period on new releases or blocking anything flagged by a published malware advisory.
- [fact] ✓ Snyk affirme que 48 % du code généré par IA contient des vulnérabilités et qu'environ six vulnérabilités sont introduites pour une corrigée.
  > Snyk’s own data shows roughly six new vulnerabilities introduced for every one remediated, and agentic development keeps widening that gap.

**Notes de fiabilité** : Article de blog d'éditeur promouvant ses propres produits (conflit d'intérêts) ; ton marketing. Les statistiques (48 %, six pour un, gains de benchmark, résultats clients) manquent de méthodologie, de références de base ou de sources, hormis un rapport cité mais non fourni. L'incident keyv et la divulgation d'Anthropic sont rapportés de seconde main, sans liens, indicateurs techniques ni détails de reproduction ; le modèle et les jeux de données du benchmark ne sont pas précisés. L'affirmation selon laquelle l'analyse de Snyk aurait évité l'exposition de l'éditeur n'est pas vérifiée. Seul un identifiant d'avis Snyk (SNYK-JS-KEYV-18515941) est donné ; aucun CVE n'apparaît. L'article indique que l'incident était en cours, de sorte que les chiffres peuvent évoluer. Le type de source est secondaire.

---

## Snyk détecte de l'injection de prompt dans 36 % des skills et 1467 charges malveillantes dans l'étude ToxicSkills sur la compromission de la chaîne d'approvisionnement des Agent Skills

- **URL**: https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/
- **Publisher**: Snyk (Snyk) | **Language**: en | **Date**: 2026-02-05
- **Type de source**: secondary | **Fiabilité a priori**: 3/5 | **Review**: draft
- **Texte analysé**: full_text | **Citations vérifiées**: 10/10
- **Tags**: agent-skills, supply-chain, prompt-injection, ClawHub, OpenClaw, Claude Code, Cursor, mcp-scan, credential-theft, malware, IOC | **Taxonomy**: AI agent supply chain security > Malicious and vulnerable agent skills > Agent Skills (SKILL.md), ClawHub, skills.sh, mcp-scan > Auditing and vetting third-party skills for AI coding agents > emerging

**Résumé**
1. Snyk a analysé 3 984 agent skills provenant de ClawHub et skills.sh ; 534 (13,4 %) présentaient au moins un problème critique.
2. 1 467 skills (36,82 %) présentaient au moins une faille de sécurité, quelle que soit la gravité.
3. Une revue humaine a confirmé 76 charges malveillantes ; 8 étaient encore en ligne sur clawhub.ai au moment de la publication.
4. Techniques d'attaque : téléchargement de malware externe, exfiltration obfusquée, et instructions de désactivation de la sécurité ou destructrices.
5. Snyk recommande d'auditer les skills installés, de renouveler les identifiants et d'utiliser son outil mcp-scan et d'autres produits Snyk.

**Enseignement**: Les agent skills (fichiers SKILL.md) s'exécutent avec les permissions complètes de l'agent de codage hôte (shell, système de fichiers, identifiants, mémoire persistante) et, selon le document, peuvent être publiés avec très peu de friction : un fichier Markdown et un compte GitHub vieux d'une semaine, sans signature de code, revue de sécurité ni sandbox par défaut. Pour une équipe utilisant des agents tels que Claude Code ou Cursor, les skills tiers constituent donc un risque de chaîne d'approvisionnement comparable à celui de paquets non vérifiés, avec en plus le problème que l'injection de prompt en langage naturel peut échapper aux scanners basés sur le code. Les chiffres proviennent d'un éditeur ayant un intérêt commercial, mais les IOC et les schémas d'attaque sont assez concrets pour agir.

**Action recommandée**: Inventoriez tous les agent skills installés par l'équipe, supprimez ceux correspondant aux auteurs et noms de skills listés, et renouvelez les identifiants auxquels ces agents pouvaient accéder. Vérifiez l'absence de modifications non autorisées dans les fichiers de mémoire des agents (SOUL.md, MEMORY.md). N'autorisez que des skills examinés, et traitez l'installation d'un skill comme l'adoption d'une dépendance. Envisagez d'exécuter mcp-scan, et vérifiez indépendamment ses résultats avant de vous y fier.

**Affirmations clés**
- [fact] ✓ Snyk a analysé 3 984 skills et en a trouvé 534 (13,4 %) avec au moins un problème de niveau critique.
  > 13.4% of all skills, or 534 in total, all contain at least one critical-level security issue, including malware distribution, prompt injection attacks, and exposed secrets.
- [fact] ✓ 36,82 % des skills analysés (1 467) présentaient au moins une faille de sécurité, quelle que soit la gravité.
  > 36.82% (1,467 skills) have at least one security flaw, from hardcoded API keys and insecure credential handling to dangerous third-party content exposure.
- [fact] ✓ Une revue avec intervention humaine (HITL) a confirmé 76 charges malveillantes, dont 8 étaient encore publiquement disponibles sur clawhub.ai au moment de la publication.
  > we confirmed active threats through HITL: 76 malicious payloads designed for credential theft, backdoor installation, and data exfiltration.
- [fact] ✓ Publier un skill sur ClawHub ne nécessite qu'un fichier Markdown et un compte GitHub vieux d'une semaine, sans signature, revue ni sandbox par défaut.
  > A SKILL.md Markdown file and a GitHub account that's one week old. No code signing. No security review. No sandbox by default.
- [analysis] ✓ Les skills héritent des permissions complètes de l'agent qu'ils étendent, ce qui les rend plus privilégiés que les paquets traditionnels.
  > Unlike traditional packages that execute in isolated contexts, Agent Skills operate with the full permissions of the AI agent they extend.
- [analysis] ✓ Parmi les skills malveillants confirmés, 100 % contiennent des schémas de code malveillant et 91 % utilisent aussi l'injection de prompt, une combinaison que, selon Snyk, les scanners de code traditionnels ne peuvent pas traiter.
  > 100% of confirmed malicious skills contain malicious code patterns, while 91% simultaneously employ prompt injection techniques.
- [fact] ✓ Snyk indique que ses détecteurs de niveau CRITICAL atteignent un rappel de 90 à 100 % sur les skills malveillants confirmés, avec 0 % de faux positifs sur les 100 meilleurs skills de skills.sh.
  > our CRITICAL-level detectors achieve 90-100% recall on confirmed malicious skills while maintaining 0% false-positive rates on the top-100 legitimate skills from skills.sh.
- [analysis] ✓ Les skills qui récupèrent du contenu distant à l'exécution permettent aux attaquants de modifier le comportement après la revue, puisque la logique d'attaque réside sur une infrastructure contrôlée par l'attaquant.
  > The published skill appears benign during review. But attackers can modify behavior at any time by updating the fetched content.
- [recommendation] ✓ Les utilisateurs devraient auditer les skills installés, supprimer les skills malveillants nommés, renouveler les identifiants et examiner les fichiers de mémoire des agents.
  > Review memory files (SOUL.md, MEMORY.md) for unauthorized modifications, given that malicious skills can poison agent memory for persistence
- [hypothesis] ✓ L'auteur zaycv serait responsable de plus de 40 skills suivant un schéma programmatique identique, ce qui suggère une génération automatisée de malware à grande échelle.
  > User zaycv: Responsible for 40+ skills following an identical programmatic pattern. This appears to be automated malware generation at scale.

**Notes de fiabilité**: Blog d'éditeur : Snyk vend mcp-scan, AI-BOM et Evo, et l'article se termine par de la promotion de produits, ce qui constitue un conflit d'intérêts évident. Les chiffres de détection et de rappel sont auto-déclarés. L'ensemble « confirmé malveillant » a été étiqueté par la propre revue humaine de Snyk et utilisé aussi pour mesurer le rappel, d'où un possible raisonnement circulaire. La méthodologie complète et le jeu de données seraient sur GitHub, mais ce rapport n'a pas été fourni. Le jeu de données n'est pas dédupliqué entre les paires auteur/ID de skill, de sorte que les skills malveillants republiés sont comptés séparément et peuvent gonfler les chiffres. Le jeu de données est aussi incohérent : le texte indique 3 984 skills issus de ClawHub et skills.sh, tandis que la section des résultats mentionne ClawHub uniquement. L'affirmation d'une « probabilité de 13 % » pour tout skill installé est une extrapolation rhétorique. Le document précise qu'il ne suppose pas que chaque skill malveillant ait mené à une compromission réussie, et aucun nombre de victimes n'est donné. Les exemples de code et le contenu des flux d'attaque semblent absents du texte. Le document cite aussi OpenSourceMalware.com pour une campagne de plus de 30 skills malveillants, mais sans la dater de façon cohérente. Aucun CVE n'est cité.

---

## Importing Phantoms: Measuring LLM Package Hallucination Vulnerabilities

- **URL**: https://arxiv.org/abs/2501.19012v1
- **Publisher**: arXiv cs.CR (arXiv (cs.CR / cs.LG listing); authors not stated) | **Language**: en | **Date**: 2025-01-31
- **Type de source**: primary | **Fiabilité a priori**: 3/5 | **Review**: draft
- **Texte analysé**: full_text | **Citations vérifiées**: 6/6
- **Tags**: package hallucination, supply chain, LLM, coding assistants, slopsquatting, HumanEval, arXiv | **Taxonomy**: Software supply chain security > LLM package hallucination > Large language models for code generation > AI-assisted software development dependency management > emerging

**Résumé**
1. Étude de l'hallucination de paquets par les LLM dans les langages de programmation courants.
2. Couvre à la fois les références à des paquets existants et les dépendances fictives.
3. Le taux d'hallucination dépend du modèle, du langage, de la taille du modèle et de la spécificité de la tâche.
4. La frontière de Pareto entre performance du code et hallucination est faiblement peuplée.
5. Une corrélation inverse est observée entre le taux d'hallucination et le score HumanEval.

**Enseignement** : Les agents de codage qui suggèrent ou installent des dépendances peuvent être poussés à importer des paquets inexistants ou enregistrés par un attaquant, ce qui élargit la surface d'attaque de la chaîne d'approvisionnement logicielle. Le résumé laisse entendre que le choix du modèle, le langage, la taille et la spécificité du prompt influencent le risque, et que HumanEval pourrait servir d'heuristique approximative. Une équipe de développement devrait traiter les dépendances suggérées par l'IA comme des entrées non fiables. Seul le résumé est disponible ; les méthodes, les chiffres et les détails des attaques ne sont donc pas indiqués.

**Action recommandée** : Lire l'article complet pour obtenir la méthodologie, les taux d'hallucination et les défenses proposées. En attendant, ajouter une étape de vérification des paquets suggérés par l'IA (existence, provenance, liste d'autorisation) avant leur installation dans les flux de travail des agents.

**Affirmations clés**
- [analysis] ✓ La tendance des LLM à halluciner du code peut être exploitée par des acteurs malveillants pour introduire des vulnérabilités dans la chaîne d'approvisionnement logicielle.
  > their tendency to hallucinate code can be used by malicious actors to introduce vulnerabilities to broad swathes of the software supply chain
- [fact] ✓ Les auteurs ont analysé l'hallucination de paquets dans les langages de programmation courants, en couvrant à la fois les références à des paquets existants et les dépendances fictives.
  > we analyze package hallucination behaviour in LLMs across popular programming languages examining both existing package references and fictional dependencies
- [fact] ✓ Le taux d'hallucination de paquets dépend du choix du modèle, du langage de programmation, de la taille du modèle et de la spécificité de la demande de codage.
  > package hallucination rate is predicated not only on model choice, but also programming language, model size, and specificity of the coding task request
- [analysis] ✓ La frontière de Pareto faiblement peuplée suggère que les modèles de codage ne sont pas optimisés pour produire du code sécurisé.
  > The Pareto optimality boundary between code generation performance and package hallucination is sparsely populated, suggesting that coding models are not being optimized for secure code.
- [fact] ✓ Le taux d'hallucination est inversement corrélé au score HumanEval, ce qui offre une heuristique pour évaluer la propension d'un modèle à halluciner des paquets.
  > we find an inverse correlation between package hallucination rate and the HumanEval coding benchmark, offering a heuristic for evaluating the propensity of a model to hallucinate packages
- [recommendation] ✓ Les auteurs identifient des attaques potentielles et suggèrent des stratégies défensives.
  > we find potential attacks and suggest defensive strategies to defend against these attacks

**Notes de fiabilité** : Source primaire, mais seule la page du résumé a été fournie ; le corps du texte, la méthodologie, les modèles testés, les tailles d'échantillon, les résultats quantitatifs et les défenses ne sont pas indiqués. Prépublication (v1) sans indication de relecture par les pairs. Les affirmations ne peuvent être vérifiées ni reproduites de manière indépendante à partir de ce texte. La corrélation avec HumanEval est présentée comme une heuristique, et non comme un résultat causal. Aucun conflit d'intérêts n'est visible, mais les auteurs et leurs affiliations ne sont pas indiqués. La page est classée sous cs.LG dans le contexte de navigation, alors que l'étiquette de la source indique cs.CR.

---
