---
# Example profile for contributors. Aang is a fictional character, not an AIX member.
# Copy _team/template.md for an actual team member; this profile demonstrates a published example.
layout: team_member
name: "Avatar Aang"
title: "Avatar and Air Nomad"
image: "aang.jpeg"
job_category: "researcher" # Example of a category used by the team page; not Aang's real affiliation.
published: true
permalink: /team/avatar-aang/
email: "im.nurmatov@gmail.com"

# These optional fields demonstrate how longer profile details can be stored.
# The body below chooses what visitors actually see on the page.
bio: >-
  Aang is the last surviving Air Nomad in Avatar: The Last Airbender.
  As the Avatar, he learns to bend all four elements and seeks to restore
  balance during the Hundred Year War.
research_interests:
  - Air Nomad culture and spirituality
  - Peaceful conflict resolution
  - Mastery of air, water, earth, and fire
website: "https://www.paramountplus.com/shows/avatar-the-last-airbender/"
---

> **Example profile:** Aang is a fictional character from *Avatar: The Last Airbender*, not a member of the AIX research group. This published example demonstrates how to fill out a team page; real profiles must contain verified information about actual group members.

## About

{{ page.bio }} He grew up at the Southern Air Temple and became an airbending master while still a child. After spending a century frozen in an iceberg with his flying bison, Appa, he returned to a world changed by the Fire Nation's war. Katara and Sokka found him and became his first companions on the journey to end the conflict.

## Background and skills

- **Home and culture:** Southern Air Temple; Air Nomad.
- **Age at the start of the story:** 12, although a century passes while he is frozen in the iceberg.
- **Role:** The Avatar, responsible for balance among the four nations.
- **Bending:** Airbending first; later waterbending, earthbending, and firebending.
- **Teachers and allies:** Monk Gyatso is an important mentor from his childhood. Katara helps him learn waterbending, Toph teaches him earthbending, and Zuko later helps him learn firebending.
- **Companions:** Appa, his flying bison, and Momo, a winged lemur.
- **Approach:** Playful, compassionate, and committed to finding peaceful solutions where possible.

## Story highlights

1. Aang learns that he is the Avatar and must master the other elements.
2. Katara and Sokka discover him after his long time in the iceberg.
3. He travels with his friends to confront the Fire Nation and restore balance.

## Interests

{% for interest in page.research_interests %}
- {{ interest }}
{% endfor %}

## More information

- [Series overview on Paramount+]({{ page.website }})
- [Story timeline from Avatar Studios](https://www.avatarstudiosofficial.com/timeline/)
- [Episode descriptions on Paramount+](https://www.paramountplus.com/shows/avatar-the-last-airbender/episodes/)

For a real team member, replace every fictional detail with verified information. Add `email`, `office`, `github`, or `linkedin` only when the person has provided accurate details. Project and publication links appear automatically below the profile when those records list the same person by name.
