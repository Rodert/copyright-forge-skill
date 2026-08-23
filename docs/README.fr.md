# Copyright Forge Skill

> Préparer des brouillons de pièces pour l'enregistrement chinois du droit d'auteur logiciel à partir de preuves issues d'un projet réel.

[简体中文](../README.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Русский](README.ru.md) | [Français](README.fr.md)

Copyright Forge est un AI Agent Skill destiné à l'enregistrement chinois du
droit d'auteur logiciel. Il extrait des preuves traçables d'un projet réel,
unifie les informations du logiciel et aide à préparer la documentation, les
pièces d'identification du code source et un brouillon des informations de
demande.

## À donner directement à votre Agent

```text
Installez et utilisez Copyright Forge Skill depuis https://github.com/Rodert/copyright-forge-skill.

Lisez skills/copyright-forge/SKILL.md, puis préparez les brouillons de pièces pour l'enregistrement chinois du droit d'auteur logiciel à partir de mon projet réel.

Avant la première préparation de pièces de chaque jour, vérifiez les mises à jour Git amont du Skill. Si le répertoire de travail est propre et qu'une mise à jour existe, appliquez-la d'abord par fast-forward. Ne signalez rien lorsqu'il est à jour. Si la vérification ou la mise à jour échoue, ou si des modifications locales bloquent la mise à jour, expliquez la raison et ne préparez pas les pièces. N'écrasez jamais les modifications locales.

Utilisez uniquement les preuves du projet réel et les faits que je confirme. N'inventez ni fonctionnalités, ni code source, ni captures d'écran, ni titulaire des droits, ni relation de développement, ni fait de publication, ni date. Ne modifiez pas le projet ou les formulaires officiels, et ne promettez pas l'approbation de l'enregistrement. Écrivez les résultats dans un répertoire distinct hors du projet et signalez les informations nécessitant ma confirmation.
```

## Fonctionnalités

- Analyse de projets Go, Java, Python, Node.js, Vue et React.
- Mise en correspondance des fonctionnalités candidates avec le code, les routes, les modèles ou les pages.
- Un unique `software-profile.yaml` pour le nom, la version et les faits confirmés.
- Liste déterministe des sources pour le dépôt ordinaire, masquage dans les seules copies générées et validation de cohérence.

## Limites de confiance

Ce Skill ne soumet pas de demande, ne détermine pas les faits juridiques, ne
modifie pas les formulaires officiels et ne garantit pas l'approbation. La
version actuelle vise le dépôt ordinaire ; les exceptions et les droits complexes
doivent être examinés manuellement.

Le point d'entrée est [SKILL.md](../skills/copyright-forge/SKILL.md). Consultez
le [README chinois](../README.md) pour les exemples de commandes et les détails.
