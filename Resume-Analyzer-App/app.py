from flask import Flask, render_template, request
import PyPDF2
import re

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        field = request.form.get("field")
        file = request.files["resume"]

        if file and file.filename.endswith(".pdf"):
            # ---------- Extract Text ----------
            pdf_reader = PyPDF2.PdfReader(file)
            extracted_text = ""

            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text

            text_lower = extracted_text.lower()
            word_count = len(extracted_text.split())

            # ---------- Field Based Skills ----------
            field_skills = {
    # TECHNICAL/DEVELOPMENT
    "software": [
        "python", "java", "c++", "c", "javascript", 
        "data structures", "algorithms", "oop", "design patterns",
        "git", "github", "debugging", "testing", "agile", "scrum"
    ],
    
    "web": [
        "html", "css", "javascript", "react", "angular", "vue",
        "node", "express", "mongodb", "sql", "api", "rest api",
        "frontend", "backend", "responsive design", "git"
    ],
    
    "mobile": [
        "react native", "flutter", "swift", "kotlin", "android",
        "ios", "mobile development", "firebase", "api integration",
        "ui/ux", "responsive design", "app store", "play store"
    ],
    
    # DATA & ANALYTICS
    "data_science": [
        "python", "r", "machine learning", "deep learning", "ai",
        "tensorflow", "keras", "pytorch", "scikit-learn",
        "statistics", "mathematics", "neural networks", "nlp"
    ],
    
    "data_analyst": [
        "sql", "excel", "python", "r", "tableau", "power bi",
        "data visualization", "statistics", "pandas", "numpy",
        "analytics", "reporting", "dashboard", "etl", "data cleaning"
    ],
    
    # INFRASTRUCTURE & SECURITY
    "devops": [
        "docker", "kubernetes", "jenkins", "ci/cd", "aws", "azure",
        "terraform", "ansible", "linux", "bash", "git", "monitoring",
        "cloud computing", "automation", "deployment", "infrastructure"
    ],
    
    "cybersecurity": [
        "network security", "penetration testing", "ethical hacking",
        "firewalls", "cryptography", "vulnerability assessment",
        "security analysis", "incident response", "risk management",
        "compliance", "siem", "ids/ips", "kali linux"
    ],
    
    # DESIGN & CREATIVE
    "ui_ux_design": [
        "figma", "sketch", "adobe xd", "photoshop", "illustrator",
        "ui design", "ux design", "prototyping", "wireframing",
        "user research", "usability testing", "design systems",
        "typography", "color theory", "responsive design"
    ],
    
    # BUSINESS & MANAGEMENT
    "digital_marketing": [
        "seo", "sem", "google analytics", "google ads", "facebook ads",
        "social media marketing", "content marketing", "email marketing",
        "copywriting", "marketing strategy", "conversion optimization",
        "analytics", "social media", "campaigns"
    ],
    
    "product_manager": [
        "product strategy", "roadmap", "agile", "scrum", "jira",
        "user stories", "market research", "analytics", "sql",
        "stakeholder management", "prioritization", "wireframing",
        "a/b testing", "data analysis", "leadership"
    ],
    
    # ENGINEERING
    "core_engineering": [
        "autocad", "solidworks", "ansys", "matlab", "catia",
        "cad", "fea", "cfd", "mechanical design", "thermodynamics",
        "manufacturing", "3d printing", "prototyping", "gd&t"
    ]
}

            required_skills = field_skills.get(field, [])

            # Find matched skills
            found_skills = []
            for skill in required_skills:
                if skill in text_lower:
                    found_skills.append(skill.title())

            matched_skills = found_skills
            missing_skills = [skill.title() for skill in required_skills if skill not in text_lower]

            matched_count = len(matched_skills)
            total_required = len(required_skills)

            if total_required > 0:
                skill_match_percent = int((matched_count / total_required) * 100)
            else:
                skill_match_percent = 0

            # ---------- Skill Strength ----------
            if skill_match_percent >= 75:
                skill_strength = "Excellent"
            elif skill_match_percent >= 50:
                skill_strength = "Good"
            elif skill_match_percent >= 30:
                skill_strength = "Moderate"
            else:
                skill_strength = "Weak"

            # ---------- Section Detection ----------
            sections_found = {
                "Education": any(keyword in text_lower for keyword in ["education", "university", "degree", "bachelor", "master"]),
                "Experience": any(keyword in text_lower for keyword in ["experience", "worked", "internship", "job"]),
                "Projects": "project" in text_lower,
                "Skills": any(keyword in text_lower for keyword in ["skills", "technical skills", "technologies"]),
                "Certifications": any(keyword in text_lower for keyword in ["certification", "certified", "certificate"])
            }

            sections_present = sum(sections_found.values())
            total_sections = len(sections_found)

            # ---------- ATS Score Calculation ----------
            ats_score = 0

            # Check for email
            if re.search(r'[\w\.-]+@[\w\.-]+', extracted_text):
                ats_score += 15
            
            # Check for phone number
            if re.search(r'\d{10}|\(\d{3}\)\s*\d{3}-\d{4}', extracted_text):
                ats_score += 15
            
            # Proper word count
            if 300 <= word_count <= 800:
                ats_score += 25
            elif 200 <= word_count <= 1000:
                ats_score += 15
            
            # Section completeness
            ats_score += (sections_present / total_sections) * 20
            
            # Skills match contribution
            ats_score += (skill_match_percent / 100) * 25

            ats_score = min(int(ats_score), 100)

            # ---------- ATS Strength ----------
            if ats_score >= 80:
                ats_strength = "Excellent"
            elif ats_score >= 60:
                ats_strength = "Good"
            elif ats_score >= 40:
                ats_strength = "Moderate"
            else:
                ats_strength = "Weak"

            # ---------- Overall Resume Score ----------
            score = 0

            # Skill impact (40% weight)
            score += skill_match_percent * 0.4

            # Word count (15% weight)
            if 300 <= word_count <= 800:
                score += 15
            elif 200 <= word_count <= 1000:
                score += 10

            # Section presence (30% weight)
            score += (sections_present / total_sections) * 30

            # Contact info (15% weight)
            if re.search(r'[\w\.-]+@[\w\.-]+', extracted_text):
                score += 8
            if re.search(r'\d{10}', extracted_text):
                score += 7

            score = min(int(score), 100)

            # ---------- Overall Strength ----------
            if score >= 80:
                strength = "Excellent"
            elif score >= 60:
                strength = "Good"
            elif score >= 40:
                strength = "Moderate"
            else:
                strength = "Weak"

            # ---------- Feedback ----------
            feedback = []

            if word_count < 200:
                feedback.append("❌ Resume is too short. Add more detailed descriptions (aim for 300-800 words).")
            elif word_count > 1000:
                feedback.append("⚠️ Resume is too long. Try to be more concise.")
            else:
                feedback.append("✅ Word count is appropriate.")

            if matched_count < 3:
                feedback.append(f"❌ Only {matched_count} key skills found. Add more relevant technical skills.")
            elif matched_count < 5:
                feedback.append(f"⚠️ {matched_count} skills matched. Consider adding more.")
            else:
                feedback.append(f"✅ Great! {matched_count} relevant skills found.")

            if not sections_found["Education"]:
                feedback.append("❌ Education section missing or not clearly labeled.")
            
            if not sections_found["Experience"] and not sections_found["Projects"]:
                feedback.append("❌ Add either Experience or Projects section to demonstrate your work.")
            
            if not sections_found["Skills"]:
                feedback.append("⚠️ Consider adding a dedicated Skills section.")

            if not re.search(r'[\w\.-]+@[\w\.-]+', extracted_text):
                feedback.append("❌ Email address not found. Add contact information.")
            
            if not re.search(r'\d{10}', extracted_text):
                feedback.append("❌ Phone number not found. Add contact information.")

            if score >= 80:
                feedback.append("🎉 Excellent resume! You're ready to apply.")
            elif score >= 60:
                feedback.append("👍 Good resume with minor improvements needed.")
            elif score >= 40:
                feedback.append("⚠️ Resume needs improvement in several areas.")
            else:
                feedback.append("❌ Resume needs major improvements before applying.")

            return render_template(
                "result.html",
                text=extracted_text,
                score=score,
                word_count=word_count,
                skills=matched_skills,
                missing_skills=missing_skills,
                feedback=feedback,
                selected_field=field,
                strength=strength,
                matched_count=matched_count,
                total_required=total_required,
                skill_match_percent=skill_match_percent,
                skill_strength=skill_strength,
                sections_found=sections_found,
                sections_present=sections_present,
                total_sections=total_sections,
                ats_score=ats_score,
                ats_strength=ats_strength
            )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)