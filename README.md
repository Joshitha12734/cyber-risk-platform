# cyber-risk-platform
AI-powered Cyber Risk Intelligence Platform that integrates vulnerability data with business context to prioritize risks, generate actionable decisions, and provide real-time insights through an interactive dashboard.
# Cyber Risk Intelligence Platform

 **Live App:**
  Secure Access

This platform includes a basic authentication layer to simulate real-world access control in cybersecurity systems.

Use the following credentials to explore the dashboard

Username: admin  
Password: crq123


https://cyber-risk-platform-8mcnbbknmnk4appjvv2d4ms.streamlit.app/

---

##  About This Project

This project started from a simple thought:

> “We detect vulnerabilities… but how do we actually decide what matters most?”

So I built a **Cyber Risk Intelligence Platform** that doesn’t just list vulnerabilities, but:

* prioritizes them
* connects them to business impact
* and explains what should be done

The goal was to move from **raw CVE data → meaningful security decisions**.

---

##  What This System Does

Instead of treating all vulnerabilities equally, this system:

* Takes real vulnerability data (NVD)
* Calculates how risky each one is
* Adjusts that risk based on where it exists (business context)
* Prioritizes what needs immediate attention
* Explains *why* it matters

---

##  How I Built It

I divided the system into clear layers so it feels like a real product, not just scripts.

---

###  1. Technical Risk Engine

This is where everything starts.

* Loads CVE data
* Calculates risk using:

  * likelihood (attack vector, complexity)
  * impact (CVSS score)

 Output: **technical risk score**

---

###  2. Contextual Risk Engine

This is the important part.

I didn’t want risk to be purely technical, so I added:

* Business criticality (High / Medium / Low)
* Internet exposure (Yes / No)

 This converts:

> “This vulnerability is bad”
> into
> “This vulnerability is dangerous *for this specific asset*”

---

###  3. Prioritization & Decision Layer

Once risks are calculated:

* CVEs are ranked
* Priority is assigned
* SLA is defined (how fast to fix)
* Decisions are suggested:

  * Approve
  * Escalate
  * Reject

 This mimics how real security teams work.

---

###  4. AI Explanation Layer

One big gap in security tools is **understanding**.

So I added:

* Human-readable explanations
* Business impact descriptions

 So even a non-technical stakeholder can understand:

> what happened and why it matters

---

###  5. Dashboard (Streamlit)

Finally, everything is visualized.

There are 3 views:

*  Executive View → overall risk picture
*  Analyst View → operational monitoring
*  Deep Dive → detailed CVE investigation

Includes:

* filters
* asset-level insights
* risk distribution
* downloadable reports

---

##  Project Structure

```
cyber-risk-platform/
│
├── Engine/              # Core logic
├── Outputs/             # Generated risk data
├── Dashboard/           # Streamlit app

```

---

##  Running It Locally

```bash
pip install streamlit pandas

python Engine/risk_engine.py
python Engine/risk_contextualizer.py

streamlit run Dashboard/app.py
```

---

##  What I Focused On

While building this, I focused on:

* Making it feel like a **real product**
* Keeping logic modular and clean
* Bridging **technical risk ↔ business impact**
* Adding explainability (not just numbers)

---

##  What Makes This Different

This is not just:

> “Here are some vulnerabilities”

Instead, it answers:

* What should I fix first?
* Why is it important?
* What happens if I ignore it?

 That shift is what I wanted to build.

---

##  Where This Can Be Used

* SOC teams
* Vulnerability management workflows
* Risk-based prioritization systems
* Security dashboards

---


##  If you liked this

Feel free to star the repo or check out the live demo!

---
