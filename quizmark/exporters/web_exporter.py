from __future__ import annotations

import json

from quizmark.models import QuizData


def export_web_package(quiz: QuizData) -> dict[str, str]:
    data = json.dumps(quiz.to_dict(), indent=2)
    return {
        "index.html": _html_template(),
        "quizmark.css": _css(),
        "quizmark.js": _js(),
        "quiz.json": data,
    }


def _html_template() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>QuizMark</title>
  <link rel="stylesheet" href="quizmark.css">
</head>
<body>
  <main id="quizmark-root"></main>
  <script src="quizmark.js"></script>
</body>
</html>
"""


def _css() -> str:
    return """body {
  margin: 0;
  font-family: var(--qm-font, "Georgia", serif);
  background: var(--qm-background, radial-gradient(circle at top, #f5f0e6, #efe7da));
  color: var(--qm-foreground, #2a2a2a);
}

#quizmark-root {
  max-width: 820px;
  margin: 0 auto;
  padding: var(--qm-spacing, 2rem) 1.5rem 3rem;
}

.qm-card {
  background: #ffffff;
  border-radius: var(--qm-radius, 20px);
  padding: 1.75rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
  margin-bottom: 1.5rem;
}

.qm-title {
  font-family: "Palatino", "Times New Roman", serif;
  font-size: 2.4rem;
  margin: 0 0 1.5rem;
}

.qm-question {
  margin: 0 0 1.25rem;
  font-size: 1.25rem;
}

.qm-answers {
  display: grid;
  gap: 0.75rem;
}

.qm-media {
  margin-top: 0.5rem;
}

.qm-answer {
  border: 1px solid #ddd;
  border-radius: 12px;
  padding: 0.75rem 1rem;
  transition: transform 120ms ease, border-color 120ms ease;
}

.qm-answer:hover {
  transform: translateY(-2px);
  border-color: var(--qm-accent, #b07d4f);
}

.qm-answer img,
.qm-question img,
.qm-answer video,
.qm-question video {
  max-width: 100%;
  border-radius: 12px;
  margin-top: 0.5rem;
}

.qm-answer audio,
.qm-question audio {
  width: 100%;
  margin-top: 0.5rem;
}

.qm-media-link {
  color: inherit;
  text-decoration: underline;
}

@media (max-width: 600px) {
  #quizmark-root {
    padding: 1.5rem 1rem 2rem;
  }
  .qm-title {
    font-size: 2rem;
  }
}
"""


def _js() -> str:
    return """async function loadQuiz() {
  const response = await fetch("quiz.json");
  const quiz = await response.json();
  applyTheme(quiz.theme);
  renderQuiz(quiz);
}

function applyTheme(theme) {
  if (!theme || !theme.properties) {
    return;
  }
  const root = document.documentElement;
  const tokens = theme.properties;
  if (tokens.background) {
    root.style.setProperty("--qm-background", tokens.background);
  }
  if (tokens.foreground) {
    root.style.setProperty("--qm-foreground", tokens.foreground);
  }
  if (tokens.accent) {
    root.style.setProperty("--qm-accent", tokens.accent);
  }
  if (tokens.font) {
    root.style.setProperty("--qm-font", tokens.font);
  }
  if (tokens.spacing) {
    root.style.setProperty("--qm-spacing", tokens.spacing);
  }
  if (tokens.radius) {
    root.style.setProperty("--qm-radius", tokens.radius);
  }
}

function renderQuiz(quiz) {
  const root = document.getElementById("quizmark-root");
  root.innerHTML = "";

  const title = document.createElement("h1");
  title.className = "qm-title";
  title.textContent = quiz.title;
  root.appendChild(title);

  if (quiz.media && quiz.media.length) {
    quiz.media.forEach((media) => {
      root.appendChild(renderMedia(media));
    });
  }

  quiz.questions.forEach((question, index) => {
    const card = document.createElement("section");
    card.className = "qm-card";

    const qTitle = document.createElement("h2");
    qTitle.className = "qm-question";
    qTitle.textContent = `${index + 1}. ${question.text}`;
    card.appendChild(qTitle);

    if (question.media) {
      question.media.forEach((media) => {
        card.appendChild(renderMedia(media));
      });
    }

    const list = document.createElement("div");
    list.className = "qm-answers";

    question.answers.forEach((answer) => {
      const item = document.createElement("div");
      item.className = "qm-answer";
      item.textContent = `${answer.label}. ${answer.text || ""}`;

      if (answer.media) {
        answer.media.forEach((media) => {
          item.appendChild(renderMedia(media));
        });
      }

      list.appendChild(item);
    });

    card.appendChild(list);
    root.appendChild(card);
  });
}

function renderMedia(media) {
  const wrapper = document.createElement("div");
  wrapper.className = "qm-media";
  if (media.kind === "image") {
    const img = document.createElement("img");
    img.src = media.value;
    img.alt = "Image";
    wrapper.appendChild(img);
  } else if (media.kind === "audio") {
    const audio = document.createElement("audio");
    audio.controls = true;
    audio.src = media.value;
    wrapper.appendChild(audio);
  } else if (media.kind === "video") {
    const video = document.createElement("video");
    video.controls = true;
    video.src = media.value;
    wrapper.appendChild(video);
  } else if (media.kind === "attachment") {
    const link = document.createElement("a");
    link.className = "qm-media-link";
    link.href = media.value;
    link.textContent = "Attachment";
    wrapper.appendChild(link);
  } else if (media.kind === "math") {
    const math = document.createElement("div");
    math.className = "qm-math";
    math.textContent = `\\(${media.value}\\)`;
    wrapper.appendChild(math);
  }
  return wrapper;
}

loadQuiz();
"""
