# Repository audit — 28 October 2026

Discovered **10 public repositories**, including the profile, through the public profile repository listing and authenticated GitHub search (`user:Moksh-dev fork:true`, pages 1 and 2). Page 2 was empty; the public web listing page 2 was also empty. Each repository metadata endpoint was fetched independently (including description, primary language and topics); all topic lists were empty. All nine project repositories were cloned and inspected individually. No private repositories are included.

The unauthenticated `/users/Moksh-dev/repos` endpoint was rate limited during the audit, and the connector does not expose the languages endpoint. Primary language metadata was obtained per repository; framework claims were checked in source/manifests. The scheduled updater uses the authenticated REST listing, full pagination and a public-count cross-check. Search discovery alone is not treated as proof that the live updater was tested.

## Code evidence

| Repository | Reviewed revision | Evidence and corrections |
| :--- | :--- | :--- |
| [AI-Sensor-House](https://github.com/Moksh-dev/AI-Sensor-House) | [0ffab23](https://github.com/Moksh-dev/AI-Sensor-House/tree/0ffab2326dbc58e77d0e54eacd91746ebc6d40d9) | README.md; src/main.cpp; platformio.ini; diagram.json; wokwi.toml. Sensor prototype, not a trained AI model. |
| [AI-Traffic-Police](https://github.com/Moksh-dev/AI-Traffic-Police) | [f805d96](https://github.com/Moksh-dev/AI-Traffic-Police/tree/f805d961cd41eb40b4233b8f6d661f78d821f814) | README.md; requirements.txt; src/detector.py; src/video_detector.py; src/vehicle_counter.py; src/dataset_evaluator.py |
| [Moksh-dev](https://github.com/Moksh-dev/Moksh-dev) | [edd651c](https://github.com/Moksh-dev/Moksh-dev/tree/edd651ce5593f4119f503d04272ba468e9f08d06) | Existing README.md, public profile bio and public Instagram link; retained software/AI/Python focus and contact identity. |
| [blackbox-dynamic](https://github.com/Moksh-dev/blackbox-dynamic) | [c6c99ec](https://github.com/Moksh-dev/blackbox-dynamic/tree/c6c99ec1413085547d77f1f3a5437ecb35057e2f) | README.md; requirements.txt; app.py routes/imports; templates. Flask/SQLAlchemy/Cloudinary confirmed. |
| [concrete-strength-model](https://github.com/Moksh-dev/concrete-strength-model) | [296901a](https://github.com/Moksh-dev/concrete-strength-model/tree/296901a0cb235db0d02c9c3030e0d7ed28c2be21) | main.py; train.csv; test.csv. The implementation uses GradientBoostingRegressor, despite a stale Random Forest comment; no README exists. |
| [one-line](https://github.com/Moksh-dev/one-line) | [8b72aa2](https://github.com/Moksh-dev/one-line/tree/8b72aa25e0110ef544c59c3166fa9299a1a6f634) | README.md; app.py; templates. Anonymous submissions, not a productivity app. |
| [project-asha](https://github.com/Moksh-dev/project-asha) | [20ce4b3](https://github.com/Moksh-dev/project-asha/tree/20ce4b3c6ae7ea0e9e808fde9601c3ffa51d5f8f) | README.md; package.json (Next.js 16, despite the older README badge); app/get-involved; lib/supabase; lib/auth/requireAdmin.ts |
| [python-calculator](https://github.com/Moksh-dev/python-calculator) | [e939f6f](https://github.com/Moksh-dev/python-calculator/tree/e939f6fa8245dbca062ffc934dd634f68ac2d75c) | README.md; calculator.py. Tkinter GUI, despite repository metadata calling it command-line. |
| [python-to-do-list](https://github.com/Moksh-dev/python-to-do-list) | [59906a4](https://github.com/Moksh-dev/python-to-do-list/tree/59906a4dacd87f2cb114f8c91222166f584319a8) | README.md; to do list.py. Tkinter, JSON storage, priorities and completion state. |
| [the-black-suits](https://github.com/Moksh-dev/the-black-suits) | [28a4b93](https://github.com/Moksh-dev/the-black-suits/tree/28a4b93f00177029804f70ffbe630336eb9d14ff) | README.md; package.json; src/App.tsx; src/Extra.tsx. Scripted sample responses and localStorage matter tracking; no live AI inference claimed. |

## Featured selection

Project ASHA demonstrates a full web application and backend integration; AI Traffic Police has a modular inference/evaluation pipeline; Concrete Strength exposes an explicit feature-engineering and regression workflow; AI Sensor House adds embedded-systems range; BLACKBOX covers Flask storage and archive interfaces; The Black Suits demonstrates a cohesive React product prototype. Smaller desktop projects and One-Line remain fully represented in the index.

## Public demos checked

- Project ASHA: https://www.project-asha.com/ — HTTP 200, page title Project ASHA.
- The Black Suits: https://theblacksuits.pythonanywhere.com/ — HTTP 200, matching project title. Labelled a prototype.
- BLACKBOX: https://mokee07.pythonanywhere.com/ — HTTP 404; omitted from README demo links.
- One-Line: https://mokee0717.pythonanywhere.com/ — HTTP 404; omitted from README demo links.
- No demo links were invented for the other projects. An HTTP check confirms the landing page, not every application feature.

GitHub and Instagram are confirmed public profile links. The connected account email is not used as a public contact source.
