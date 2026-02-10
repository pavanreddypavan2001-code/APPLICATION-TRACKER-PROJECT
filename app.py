import streamlit as st
import pandas as pd
import os
from datetime import date
from dotenv import load_dotenv
from openai import OpenAI

# 
if "chat" not in st.session_state:
    st.session_state.chat = []

# -------------------------------

st.set_page_config(
    page_title="Pavan's Job Application Tracker",
    layout="wide"
)

CSV_FILE = "jobs.csv"

# -------------------------------
# FUNCTIONS

def load_data():
    """
    Load job data from CSV.

    """
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(
            columns=["JobId",
                "Company",
                "Position",
                "Location",
                "Applied Date",
                "Status",
                "Recruiter Emails",
                "Interviews",
                "Notes"
            ]
        )

def save_data(df):
    """
    Save DataFrame to CSV file
    """
    df.to_csv(CSV_FILE, index=False)

# -------------------------------

if "jobs" not in st.session_state:
    st.session_state.jobs = load_data()

# -------------------------------
##- TITLE.

st.title("Pavan'sJob Application Tracker")
st.subheader("Total Jobs Applied")
# ✅ Total jobs applied count
total_jobs = st.session_state.jobs.shape[0]   # number of rows = total jobs applied

# Show it at the top
st.metric("📊 Total Jobs Applied", total_jobs)
# ✅ Top counts
df_top = st.session_state.jobs.copy()
df_top.columns = df_top.columns.str.strip()

total_jobs = df_top.shape[0]

# Safe numeric conversion for Interviews
if "Interviews" in df_top.columns:
    total_interviews = pd.to_numeric(df_top["Interviews"], errors="coerce").fillna(0).sum()
else:
    total_interviews = 0

# Rejected count
if "Status" in df_top.columns:
    rejected_jobs = (df_top["Status"].astype(str) == "Rejected").sum()
else:
    rejected_jobs = 0

# Show metrics at top
c1, c2, c3 = st.columns(3)
c1.metric("📊 Total Jobs Applied", total_jobs)
c2.metric("🎯 Total Interviews", int(total_interviews))
c3.metric("❌ Rejected Jobs", int(rejected_jobs))





# Get total count
total_jobs = len(st.session_state.jobs)  or st.session_state.jobs.shape[0]

# Total jobs applied
total_jobs = len(st.session_state.jobs)

# SIDEBAR - ADD JOB
# -------------------------------

st.sidebar.header("Add New Job")

company = st.sidebar.text_input("Company Name")
position = st.sidebar.text_input("Job Position")
location = st.sidebar.text_input("Location")

applied_date = st.sidebar.date_input(
    "Applied Date",
    value=date.today()
)

status = st.sidebar.selectbox(
    "Application Status",
    ["Applied", "Interview", "Offer", "Rejected"]
)

emails = st.sidebar.number_input(
    "Recruiter Emails Sent",
    min_value=0,
    step=1
)

interviews = st.sidebar.number_input(
    "Interview Rounds",
    min_value=0,
    step=1
)

notes = st.sidebar.text_area("Notes")

# -------------------------------
# ADD BUTTON
# -------------------------------

if st.sidebar.button("Add Job"):
    new_job = {
        "Company": company,
        "Position": position,
        "Location": location,
        "Applied Date": applied_date.strftime("%Y-%m-%d"),
        "Status": status,
        "Recruiter Emails": emails,
        "Interviews": interviews,
        "Notes": notes
    }

    st.session_state.jobs = pd.concat(
        [st.session_state.jobs, pd.DataFrame([new_job])],
        ignore_index=True
    )

    save_data(st.session_state.jobs)
    st.sidebar.success("Job added successfully!")
    ####


# -------------------------------
# MAIN TABLE

#---------------------------
st.subheader("All Job Applications")

df = st.session_state.jobs.copy()

edited_df = st.data_editor(
    df,
    use_container_width=True,
    num_rows="dynamic",     # allow adding rows if you want
    key="job_editor"
)

# Save changes button
if st.button("Save Edits"):
    st.session_state.jobs = edited_df
    save_data(st.session_state.jobs)
    st.success("✅ Changes saved to jobs.csv")

    

    # -------------------------------
    # IF WE WANT TO DELETE SELECTED  JOBS

    st.subheader(" Delete Job(s)")
    rows_to_delete = st.multiselect(
        "Select row index to delete:",
        df.index.tolist()
    )

    if st.button("Delete Selected Jobs"):
        st.session_state.jobs = df.drop(rows_to_delete).reset_index(drop=True)
        save_data(st.session_state.jobs)
        st.success("Selected jobs deleted")



import matplotlib.pyplot as plt

###--------------------------------------
st.subheader(" Jobs Count by Date")

# Ensure Applied Date is datetime
df = st.session_state.jobs.copy()
df["Applied Date"] = pd.to_datetime(df["Applied Date"])

# Count jobs per day
jobs_per_day = df.groupby("Applied Date").size().reset_index(name="Total Jobs")

# Display table
st.dataframe(jobs_per_day)
###-----------------------------------------###

# 
###--------####-----####------#####-------
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Job Application Analytics Dashboard")

# Use latest jobs data
df = st.session_state.jobs.copy()
df["Applied Date"] = pd.to_datetime(df["Applied Date"])

# Count jobs by status
status_counts = df["Status"].value_counts()

# Count jobs per day
jobs_per_day = df.groupby("Applied Date").size().sort_index()

# Define color mapping
color_map = {"Applied": "blue", "Interview": "orange", "Offer": "green", "Rejected": "red"}
colors = [color_map.get(status, "gray") for status in status_counts.index]

# ---------- Layout: 2 columns ----------
col1, col2 = st.columns(2)

# --- PIE CHART ---
with col1:
    st.subheader("Job Status Pie Chart")
    fig1, ax1 = plt.subplots()
    ax1.pie(status_counts, labels=status_counts.index, colors=colors,
            autopct="%1.1f%%", startangle=90)
    ax1.axis("equal")
    if st.button("Enlarge Pie Chart"):
        st.pyplot(fig1)
    else:
        st.pyplot(fig1)

# --- BAR CHART ---
with col2:
    st.subheader("Job Status Bar Chart")
    fig2, ax2 = plt.subplots()
    bars = ax2.bar(status_counts.index, status_counts.values, color=colors)
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, height + 0.1, str(int(height)),
                 ha='center', va='bottom', fontsize=12)
    ax2.set_ylabel("Number of Jobs")
    if st.button("Enlarge Bar Chart"):
        st.pyplot(fig2)
    else:
        st.pyplot(fig2)

# ---------- ---
    df = st.session_state.jobs.copy()
    ##### TO GET THE IDEA OF THE REJECTIONS LIKE REASONS FOR THE REJECTIONS 
    ##### SO WE WIL HAVE AN IDEA WHATS GOING WRONG ,,SO WE CAN MAKE IMPROVEMENTS IN THAT AREA.

st.divider()
st.subheader("REASONS FOR THE REJECTIONS")

# Filter only rejected jobs
rejected_df = df[df["Status"] == "Rejected"]

if rejected_df.empty:
    st.info("No rejected jobs available for analysis yet.")
else:
    # Define rejection categories with keywords
    rejection_rules = {
        "Resume Issue": ["resume", "cv", "not shortlisted"],
        "Experience Issue": ["experience", "years", "senior"],
        "Skill Mismatch": ["skill", "mismatch", "technology"],
        "Visa / Location Issue": ["visa", "location", "relocation"],
        "Position Closed": ["position closed", "role closed"],
         
          "Coding round Failed": ["coding round failed"],
           "technical round": ["technical round"],
            "screening round": ["screening round"],
             "Final round": ["final round"],
        "No Response / Other": []
    }

    # Dictionary to store counts      
    rejection_counts = {}

    # Analyze each rejection note
    for note in rejected_df["Notes"].fillna(""):
        note = note.lower()
        matched = False

        for reason, keywords in rejection_rules.items():
            for keyword in keywords:
                if keyword in note:
                    rejection_counts[reason] = rejection_counts.get(reason, 0) + 1
                    matched = True
                    break
            if matched:
                break

        if not matched:
            rejection_counts["No Response / Other"] = (
                rejection_counts.get("No Response / Other", 0) + 1
            )

    # Convert results to DataFrame
    rejection_summary = pd.DataFrame(
        rejection_counts.items(),
        columns=["Rejection Reason", "Count"]
    )

    # Show table
    st.subheader(" Rejection Summary Table")
    st.dataframe(rejection_summary, use_container_width=True)
    #___
    # ===========================
# ML + Improvements + Move Chat Input
# ===========================

st.divider()
st.subheader("🧠 ML: Job Success Probability + Improvement Tips")

df_ml = st.session_state.jobs.copy()

# --- Basic cleaning / features ---
# Convert Applied Date
if "Applied Date" in df_ml.columns:
    df_ml["Applied Date"] = pd.to_datetime(df_ml["Applied Date"], errors="coerce")
else:
    df_ml["Applied Date"] = pd.NaT

# Ensure numeric columns
for c in ["Recruiter Emails", "Interviews"]:
    if c in df_ml.columns:
        df_ml[c] = pd.to_numeric(df_ml[c], errors="coerce").fillna(0)
    else:
        df_ml[c] = 0

# Create simple target:
# "Success" = Offer or Interview (you can adjust this logic later)
df_ml["target_success"] = df_ml["Status"].isin(["Interview", "Offer"]).astype(int)

# Features
df_ml["applied_month"] = df_ml["Applied Date"].dt.month.fillna(0).astype(int)
df_ml["applied_dow"] = df_ml["Applied Date"].dt.dayofweek.fillna(0).astype(int)

# Keep only rows where we have minimally required fields
needed_cols = ["Company", "Position", "Location", "Recruiter Emails", "Interviews", "applied_month", "applied_dow", "target_success"]
for col in ["Company", "Position", "Location"]:
    if col not in df_ml.columns:
        df_ml[col] = ""

df_train = df_ml[needed_cols].dropna()

# If not enough data, guide user
min_rows = 25
if len(df_train) < min_rows:
    st.info(f"Add at least ~{min_rows} job rows to train ML. Currently you have {len(df_train)} usable rows.")
else:
    # --- Train a lightweight model (Logistic Regression) ---
    # Using scikit-learn (install if needed: pip install scikit-learn)
    try:
        from sklearn.model_selection import train_test_split
        from sklearn.compose import ColumnTransformer
        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import OneHotEncoder, StandardScaler
        from sklearn.linear_model import LogisticRegression
        from sklearn.metrics import roc_auc_score, accuracy_score

        X = df_train.drop(columns=["target_success"])
        y = df_train["target_success"]

        cat_cols = ["Company", "Position", "Location"]
        num_cols = ["Recruiter Emails", "Interviews", "applied_month", "applied_dow"]

        pre = ColumnTransformer(
            transformers=[
                ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
                ("num", Pipeline([("scaler", StandardScaler())]), num_cols),
            ]
        )

        model = Pipeline(steps=[
            ("preprocess", pre),
            ("clf", LogisticRegression(max_iter=2000))
        ])

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

        model.fit(X_train, y_train)

        # Eval
        proba = model.predict_proba(X_test)[:, 1]
        pred = (proba >= 0.5).astype(int)

        auc = roc_auc_score(y_test, proba) if len(set(y_test)) > 1 else None
        acc = accuracy_score(y_test, pred)

        c1, c2 = st.columns(2)
        c1.metric("Model Accuracy", f"{acc:.2f}")
        if auc is not None:
            c2.metric("ROC-AUC", f"{auc:.2f}")
        else:
            c2.metric("ROC-AUC", "Not enough class variety")

        st.caption("Target = Interview/Offer treated as success. This is a starter baseline model.")

        # --- Predict for NEW / EXISTING JOB rows ---
        st.subheader("📌 Predict Probability for a New Job")

        p_company = st.text_input("Company (for prediction)", "")
        p_position = st.text_input("Position (for prediction)", "")
        p_location = st.text_input("Location (for prediction)", "")
        p_emails = st.number_input("Recruiter Emails (for prediction)", min_value=0, step=1, value=0)
        p_interviews = st.number_input("Interview Rounds (for prediction)", min_value=0, step=1, value=0)
        p_month = st.number_input("Applied Month (1-12)", min_value=1, max_value=12, step=1, value=date.today().month)
        p_dow = st.number_input("Day of Week (0=Mon ... 6=Sun)", min_value=0, max_value=6, step=1, value=date.today().weekday())

        if st.button("Predict Success Probability"):
            row = pd.DataFrame([{
                "Company": p_company,
                "Position": p_position,
                "Location": p_location,
                "Recruiter Emails": p_emails,
                "Interviews": p_interviews,
                "applied_month": int(p_month),
                "applied_dow": int(p_dow)
            }])

            prob = float(model.predict_proba(row)[:, 1][0])
            st.success(f"✅ Estimated Success Probability: **{prob*100:.1f}%**")
            

            # --- Simple improvement tips based on your data ---
            st.subheader("🔧 What to Improve (Data-driven Tips)")

            # Compare your own historical outcomes
            hist = df_train.copy()
            succ = hist[hist["target_success"] == 1]
            fail = hist[hist["target_success"] == 0]

            tips = []

            if len(succ) > 5 and len(fail) > 5:
                avg_em_s = succ["Recruiter Emails"].mean()
                avg_em_f = fail["Recruiter Emails"].mean()
                avg_int_s = succ["Interviews"].mean()
                avg_int_f = fail["Interviews"].mean()

                if avg_em_s > avg_em_f + 0.2:
                    tips.append(f"- Your successful outcomes had **more recruiter emails** on average ({avg_em_s:.1f} vs {avg_em_f:.1f}). Try increasing follow-ups.")
                else:
                    tips.append("- Recruiter email count doesn’t differ much in your history. Focus on resume/skills/interview preparation.")

                if avg_int_s >= avg_int_f:
                    tips.append(f"- Success cases show **more interview rounds** on average ({avg_int_s:.1f} vs {avg_int_f:.1f}). Keep improving interview performance to progress rounds.")

            # Use your rejection notes patterns you already built
            # (You already have rejection_summary earlier; we rebuild quick here safely)
            if "Status" in df_ml.columns and "Notes" in df_ml.columns:
                rej = df_ml[df_ml["Status"] == "Rejected"]["Notes"].fillna("").str.lower()
                resume_hits = rej.str.contains("resume|cv|not shortlisted").sum()
                exp_hits = rej.str.contains("experience|years|senior").sum()
                skill_hits = rej.str.contains("skill|mismatch|technology").sum()

                if resume_hits > 0:
                    tips.append(f"- **Resume-related** rejections detected ({resume_hits}). Improve ATS keywords + tailor resume for each role.")
                if exp_hits > 0:
                    tips.append(f"- **Experience-related** rejections detected ({exp_hits}). Target closer-fit roles + highlight relevant projects with measurable impact.")
                if skill_hits > 0:
                    tips.append(f"- **Skill mismatch** detected ({skill_hits}). Add 1–2 priority skills per target role and build mini-projects to prove them.")

            if not tips:
                tips = ["- Add more data (jobs + notes). Then I can generate stronger, personalized improvement insights."]

            st.markdown("\n".join(tips))

        # --- Optional: show probabilities for your existing rows ---
        st.subheader("📊 Predict Success Probability for Existing Jobs (Preview)")
        preview_n = st.slider("How many rows to score?", min_value=5, max_value=min(200, len(df_train)), value=min(25, len(df_train)))
        score_df = df_train.head(preview_n).drop(columns=["target_success"]).copy()
        score_df["pred_success_prob"] = model.predict_proba(score_df)[:, 1]
        st.dataframe(score_df[["Company", "Position", "Location", "Recruiter Emails", "Interviews", "pred_success_prob"]], use_container_width=True)

    except Exception as e:
        st.error("ML section needs scikit-learn installed and working.")
        st.write("Error:", e)


# ===========================
# 
# ===========================
# .
try:
    with CHAT_TOP.container():
        st.subheader("🔎 Chat Search (Top)")
        user_q2 = st.chat_input("Ask about your tracker data (top): e.g., 'show rejected jobs', 'top companies', 'interviews this month'")
        if user_q2:
            # Reuse your same chatbot logic safely
            st.session_state.chat.append({"role": "user", "content": user_q2})

            df2 = st.session_state.jobs.copy()
            context2 = jobs_to_text(df2)

            prompt2 = f"""
You are an assistant for a Job Application Tracker.
Answer using ONLY the data in this CSV (from jobs.csv). If data is missing, say so.

CSV:
{context2}

User question: {user_q2}

Rules:
- If user asks for a list, show Company | Position | Status | Applied Date.
- Keep answers clear and short.
"""
            resp2 = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt2}]
            )
            answer2 = resp2.choices[0].message.content
            st.session_state.chat.append({"role": "assistant", "content": answer2})
except NameError:
    # If CHAT_TOP isn't defined (because you didn't add the 1 line near top),
    # we fall back: show a message + optional sidebar chat input approach.
    st.info("To put chat input at the top, add this ONE line near the top: `CHAT_TOP = st.empty()`")
#############################################################################################
 # ==========================
# ALWAYS-WORKS SEARCH CHATBOT (NO LLM)
# Add this at the END of the file
# ==========================

st.divider()
st.subheader("🔎 Search Chatbot (Fast Search in Your jobs.csv)")

df_search = st.session_state.jobs.copy()
df_search.columns = df_search.columns.str.strip()

# Safety conversions
if "Applied Date" in df_search.columns:
    df_search["Applied Date"] = pd.to_datetime(df_search["Applied Date"], errors="coerce")

for col in ["Recruiter Emails", "Interviews"]:
    if col in df_search.columns:
        df_search[col] = pd.to_numeric(df_search[col], errors="coerce").fillna(0)

q = st.text_input(
    "Search like: company:amazon | status:rejected | position:data analyst | location:texas | notes:visa | interviews>0",
    key="search_box_bottom"
)

def apply_search(df, query: str):
    if not query or not query.strip():
        return df

    query = query.strip().lower()

    # Support simple operators: interviews>0, emails>=2
    ops = [(">=", ">="), ("<=", "<="), (">", ">"), ("<", "<"), ("=", "=")]

    # Split by |
    parts = [p.strip() for p in query.split("|") if p.strip()]
    out = df.copy()

    for p in parts:
        # numeric filters
        if any(op in p for _, op in ops):
            # Example: interviews>0
            for _, op in ops:
                if op in p:
                    left, right = [x.strip() for x in p.split(op, 1)]
                    try:
                        val = float(right)
                    except:
                        continue

                    # map user-friendly keys
                    key_map = {
                        "interviews": "Interviews",
                        "emails": "Recruiter Emails",
                        "recruiter emails": "Recruiter Emails",
                    }
                    col = key_map.get(left, left.title())
                    if col not in out.columns:
                        continue

                    if op == ">=":
                        out = out[out[col] >= val]
                    elif op == "<=":
                        out = out[out[col] <= val]
                    elif op == ">":
                        out = out[out[col] > val]
                    elif op == "<":
                        out = out[out[col] < val]
                    elif op == "=":
                        out = out[out[col] == val]
                    break
            continue

        # key:value filters
        if ":" in p:
            k, v = [x.strip() for x in p.split(":", 1)]
            key_map = {
                "company": "Company",
                "position": "Position",
                "location": "Location",
                "status": "Status",
                "notes": "Notes",
            }
            col = key_map.get(k, None)
            if col and col in out.columns:
                out = out[out[col].fillna("").astype(str).str.lower().str.contains(v, na=False)]
        else:
            # free text search across key columns
            text_cols = [c for c in ["Company", "Position", "Location", "Status", "Notes"] if c in out.columns]
            mask = False
            for c in text_cols:
                mask = mask | out[c].fillna("").astype(str).str.lower().str.contains(p, na=False)
            out = out[mask]

    return out

result = apply_search(df_search, q)

c1, c2, c3 = st.columns(3)
c1.metric("Total Rows", len(df_search))
c2.metric("Matched Rows", len(result))
c3.metric("Rejected Rows", int((df_search["Status"].astype(str) == "Rejected").sum()) if "Status" in df_search.columns else 0)

st.dataframe(
    result[[c for c in ["Company", "Position", "Status", "Applied Date", "Location", "Recruiter Emails", "Interviews", "Notes"] if c in result.columns]],
    use_container_width=True
)
##############
# ==========================
# WHAT SHOULD I IMPROVE / LEARN (DATA-DRIVEN)
# Add this at the END of the file
# ==========================

st.divider()
st.subheader("🎯 What Should I Improve To Increase Job Success?")

df_imp = st.session_state.jobs.copy()
df_imp.columns = df_imp.columns.str.strip()

if "Notes" not in df_imp.columns or "Status" not in df_imp.columns:
    st.info("Add Notes and Status columns to get personalized improvement suggestions.")
else:
    rej_notes = df_imp[df_imp["Status"].astype(str) == "Rejected"]["Notes"].fillna("").astype(str).str.lower()

    # detect themes
    themes = {
        "Resume / ATS": ["resume", "cv", "not shortlisted", "shortlist", "ats"],
        "Experience Framing": ["experience", "years", "senior", "overqualified", "underqualified"],
        "Skill Gaps (Core Tech)": ["skill", "mismatch", "technology", "missing", "stack"],
        "Location / Visa": ["visa", "relocation", "location", "work authorization", "sponsorship"],
        "Interview Performance": ["technical round", "coding", "screening", "final round", "behavioral", "communication"],
        "Role Closed / Timing": ["position closed", "role closed", "hiring freeze"],
        "No Response": ["no response", "ghost", "no update", "no reply"],
    }

    counts = {}
    for name, kws in themes.items():
        if len(kws) == 0:
            counts[name] = 0
        else:
            counts[name] = int(rej_notes.apply(lambda t: any(k in t for k in kws)).sum())

    # show summary
    summary = pd.DataFrame(sorted(counts.items(), key=lambda x: x[1], reverse=True), columns=["Theme", "Hits in Rejections"])
    st.dataframe(summary, use_container_width=True)

    # learning recommendations mapped to themes
    st.subheader("📚 Personalized Learning Plan (Based on Your Rejections)")

    recs = []

    if counts.get("Resume / ATS", 0) > 0:
        recs.append("**Resume / ATS**: Tailor resume per job description, add keyword match, strong project bullets with metrics, clean formatting.")

    if counts.get("Experience Framing", 0) > 0:
        recs.append("**Experience Framing**: Re-write bullets using STAR method, quantify impact, highlight relevant tools used (SQL, Python, BI), align to role level.")

    if counts.get("Skill Gaps (Core Tech)", 0) > 0:
        recs.append("**Skill Gaps (Core Tech)**: Pick 1 target role (Data Analyst / Data Engineer) and master the top skills: SQL (joins/windows), Python (pandas/EDA), BI (Power BI/Tableau), basic stats.")

    if counts.get("Interview Performance", 0) > 0:
        recs.append("**Interview Performance**: Practice 30–50 SQL questions (joins, group by, windows), 20–30 Python (pandas + coding), plus mock behavioral answers.")

    if counts.get("Location / Visa", 0) > 0:
        recs.append("**Location/Visa Strategy**: Focus on roles matching your work eligibility/location, mention it clearly, and prioritize remote/hybrid roles that fit your profile.")

    if counts.get("No Response", 0) > 0:
        recs.append("**Follow-up Strategy**: Follow-up on day 4–5, again on day 9–10. Track recruiter emails and add short value message (1 line skill fit + 1 line portfolio link).")

    if not recs:
        recs.append("No strong rejection themes detected yet. Add detailed Notes for each rejection to unlock personalized recommendations.")

    for r in recs:
        st.write("✅", r)

    # Always show a “core roadmap”
    st.subheader("✅ Core Skills Roadmap (Most Useful For Getting Hired)")
    st.markdown("""
**If you’re targeting Data Analyst / Business Analyst roles:**
- SQL: joins, group by, subqueries, CTEs, window functions
- Python: pandas, EDA, data cleaning, CSV/Excel, basic visualization
- Power BI / Tableau: dashboards, DAX basics (Power BI), storytelling
- Statistics: mean/median, variance/std dev, probability basics, A/B basics
- Communication: explain insights + business impact

**If you’re targeting Data Engineer roles:**
- SQL advanced + performance basics (indexes, query plans)
- Python: ETL scripts, APIs, file handling, logging
- Data modeling: star schema, normalization basics
- Cloud basics: S3, IAM concepts, basic pipelines
- Orchestration: Airflow fundamentals
""")
###############
# ==========================
# ==========================

if "CHAT_TOP" not in globals():
    pass


##################################--------------------##############################
st.subheader(" KEEP GOING          ")
st.subheader(" FOCUS AND TRY TO IMPROVE")
st.subheader(" ALL THE BEST")