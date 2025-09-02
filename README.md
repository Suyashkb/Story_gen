# Self-Compassion Story Experiment

This repository contains the codebase for an interactive **Self-Compassion Narrative Experiment** designed and deployed as part of an internship at the **MIND Lab, IIT Delhi**.
The goal is to study the **neural correlates of self-compassion** in young adults through **personalized storytelling**. Participants listen to personalized stories while EEG and fNIRS data are collected.

🔗 **Live App**: [https://scstory.streamlit.app](https://scstory.streamlit.app)

---

## Overview

The project aims to:

* Explore **personalization in storytelling** as a tool to elicit self-compassion.
* Capture corresponding brain activity using **EEG** and **fNIRS**.
* Provide a scalable, digital platform for long-term **self-compassion interventions**.

### Research Question

> How does personalization in short narratives influence neural correlates of self-compassion in young adults?

---

## Repository Structure

```
components/
  ├── __pycache__/
  ├── __init__.cpython-312.pyc
  ├── final_feedback.cpython-312.pyc
  ├── mindfulness.cpython-312.pyc
  ├── personalization.cpython-312.pyc
  ├── quiz.cpython-312.pyc
  └── story.cpython-312.pyc
final_feedback.py
mindfulness.py
personalization.py
quiz.py
story.py
main.py
requirements.txt
.gitignore
.devcontainer/
```

* **components/**: Contains modular code for story personalization, quiz, mindfulness tasks, and feedback.
* **main.py**: Entry point for the Streamlit app.
* **requirements.txt**: List of dependencies.

---

## Getting Started

### Prerequisites

Ensure you have Python 3.10+ installed. Install dependencies:

```bash
pip install -r requirements.txt
```

### Running Locally

Run the app locally with:

```bash
streamlit run main.py
```

Then, open your browser and navigate to the displayed local URL.

---

## Experiment Flow

1. **Consent Form**: Participants provide informed consent.
2. **Personalization Quiz**: Collects participant details to tailor the story.
3. **Mindfulness Exercise**: Prepares participants for the storytelling session.
4. **Personalized Story**: Generated based on participant input.
5. **Feedback**: Participants rate their experience.

---

## Applications

* Neuroscientific studies on self-compassion.
* Classroom-based emotional well-being interventions.
* Long-term self-compassion and empathy training.

---

## Acknowledgements

Developed by Suyash Kumar Bhagat during internship at **MIND Lab, IIT Delhi**.

---

## 📜 License

This project is licensed under the MIT License. See `LICENSE` for more details.
