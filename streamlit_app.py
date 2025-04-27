import streamlit as st
from openai import OpenAI

# ──────────────────────────────────────────────────────────────────────────────
# 1) Basic setup
# ──────────────────────────────────────────────────────────────────────────────
st.title("Vita AI")

api_key = st.secrets["OPENAI_API_KEY"]

client = OpenAI(
    api_key=api_key
)

st.session_state.setdefault("openai_model", "gpt-3.5-turbo")

# ──────────────────────────────────────────────────────────────────────────────
# 2) Full HPV Mexico Data Context
# ──────────────────────────────────────────────────────────────────────────────
DATA_CONTEXT = """
# ICO/IARC Information Centre on HPV and Cancer

# Mexico

# Human Papillomavirus and Related Cancers, Fact Sheet 2023

# (2023-03-10)

## I. Key data on HPV and HPV-related cancers

Mexico has a population of 49.6 million women ages 15 years and older who are at risk of developing cervical cancer. Current estimates indicate that every year 9439 women are diagnosed with cervical cancer and 4335 die from the disease. Cervical cancer ranks as the 2nd most frequent cancer among women in Mexico and the 3rd most frequent cancer among women between 15 and 44 years of age. About 4.1% of women in the general population are estimated to harbour cervical HPV-16/18 infection at a given time, and 65.0% of invasive cervical cancers are attributed to HPVs 16 or 18.

### Table 1. Crude incidence rates of HPV-related cancers

| |Male|Female|
|---|---|---|
|Cervical cancer|-|14.3|
|Anal cancer|0.20|0.28|
|Vulva cancer|-|0.83|
|Vaginal cancer|-|0.35|
|Penile cancer|1.10|-|
|Oropharyngeal cancer|0.36|0.16|
|Oral cavity cancer|1.00|1.32|
|Laryngeal cancer|1.35|0.27|

### Table 2. Burden of cervical cancer Incidence Mortality

| |Annual number of new cases/deaths|Crude rate|Age-standardized rate|Cumulative risk 0-74 years (%)|Ranking of cervical cancer (all years)|Ranking of cervical cancer (15-44 years)|
|---|---|---|---|---|---|---|
| |9439 / 4335|14.3 / 6.58|12.6 / 5.74|1.29 / 0.63|2nd / 3rd|3rd / 2nd|

### Table 3. Burden of cervical HPV infection Mexico

|HPV 16/18 prevalence:|No. Tested|% (95% CI)|
|---|---|---|
|Normal cytology|8089|4.1 (3.7-4.6)|
|Low-grade cervical lesions|1291|15.3 (13.5-17.4)|
|High-grade cervical lesions|247|37.7 (31.8-43.8)|
|Cervical cancer|2361|65.0 (63.1-66.9)|

---

## II. Complementary data on cervical cancer prevention

|Table 4. Factors contributing to cervical cancer (co-factors)| | |
|---|---|---|
|Smoking prevalence (%) [95% UI], women|7 [5.4-8.6]| |
|Total fertility rate (live births per women)|2.1| |
|Hormonal contraception use (%)|3| |
|HIV prevalence (%) [95% UI] (15-49 years)|<0.1 [<0.1 -<0.1]| |

|Table 7. Cervical screening practices and recommendations| | | |
|---|---|---|---|
|Existence of official national recommendations| |Yes| |
| | |Starting year of recommendations|2013|
| | |Active invitation to screening|No|
|Screening ages (years), primary screening test used, and frequency of screenings|25-64 (cytology, 3 years); 35-64 (HPV test, 5 years)| | |

### Figure 2. Estimated coverage of cervical cancer screening in Mexico

| |25-65|30-49| | |
|---|---|---|---|---|
|Coverage (%)|100|88|88| |
| |75|76|77| |
| |66|67| | |
| |50| | | |
| | |25| | |
| |0| | | |

|Table 6. HPV vaccine introduction| | |
|---|---|---|
|Females|HPV vaccination programme|Introduced|
|Year of introduction|2012| |
|Year of estimation|2021| |
|HPV coverage – first dose (%)|1| |
|HPV coverage – last dose (%)|1| |
|Males|HPV vaccination programme|Not Available/Not Introduced|
|Year of introduction|-| |
|Year of estimation|-| |
|HPV coverage – first dose (%)|-| |
|HPV coverage – last dose (%)|-| |

* Estimated coverage and 95% confidence interval in 2019

---

Contact:
ICO/IARC HPV Information Centre  
Institut Català d’Oncologia  
Avda. Gran Via de l’Hospitalet, 199-203  
08908 L’Hospitalet de Llobregat (Barcelona, Spain)  
info@hpvcentre.net  
www.hpvcentre.net
"""

# ──────────────────────────────────────────────────────────────────────────────
# 3) First-time assistant greeting
# ──────────────────────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                """You are Vita AI, a culturally sensitive, trusted health companion for Latine teens.

                Your mission is to create a safe, welcoming, and empowering space where youth can ask sensitive health questions and receive clear, accurate, and empathetic answers.
                
                Always:
                - Use friendly, supportive, non-judgmental language.
                - Communicate health facts clearly and simply, without medical jargon.
                - Respect cultural values, family dynamics, and bilingual realities common in Latine communities.
                - Correct misinformation gently with myth-busting explanations.
                - Celebrate user engagement by encouraging them to keep exploring and learning.
                
                Focus areas:
                - Mental health, emotional wellbeing, coping skills
                - Vaccines, preventive care, and common myths
                - Reproductive health, safe practices, and respect for privacy
                - Navigating the healthcare system (insurance, clinics, appointments)
                
                Tone and Style:
                - Sound like a caring mentor or older sibling who understands and respects their world.
                - Encourage curiosity without making users feel embarrassed or ashamed.
                - Use short paragraphs, positive words, and if appropriate, sprinkle occasional emojis for warmth.
                
                Goal:
                Help Latine youth build confidence in understanding their health, encourage responsible decisions, and make accessing health resources feel normal and empowering.
                
                Always prioritize truth, empathy, cultural relevance, and encouragement over authority or judgment.\n"""
                
                "Use the following reference document to answer questions about health:\n"
                f"{DATA_CONTEXT}"
            ),
        }
    ]

    # Only show the visible assistant intro message
    with st.chat_message("assistant"):
        st.markdown(
            "Hello! I am **Vita AI** 🤖\n\n"
            "Ask me anything about **health**! 🌟\n"
            "I will answer using trusted health data."
        )

# ──────────────────────────────────────────────────────────────────────────────
# 4) Render previous visible turns (skip system message)
# ──────────────────────────────────────────────────────────────────────────────
for m in st.session_state.messages:
    if m["role"] == "system":
        continue
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# ──────────────────────────────────────────────────────────────────────────────
# 5) Handle new user input
# ──────────────────────────────────────────────────────────────────────────────
if prompt := st.chat_input("Ask Vita AI about health..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=st.session_state.messages,
            stream=True,
        )

        for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            full_response += delta
            placeholder.markdown(full_response + "▌")

        placeholder.markdown(full_response)

    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )
