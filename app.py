from flask import Flask, render_template, request, redirect, url_for
import smtplib
import ssl
from email.mime.text import MIMEText
app = Flask(__name__)

# List of subjects and their syllabus and notes
subject_files = {
    1: {
        "name": "Mathematics 1",
        "units": [
            {
                "unit": 1,
                "syllabus": "UNIT - I: Matrices: Rank of a matrix by Echelon form and Normal form, Inverse of Non-singular matrices by Gauss-Jordan method, System of linear equations: Solving system of Homogeneous and Non-Homogeneous equations by Gauss elimination method, Gauss Seidel Iteration Method.",
                "notes": [{"name": "Unit 1 Matrices notes", "file_path": "https://drive.google.com/file/d/1AIbD0d3OkxipBe9_kBsk32ecZ4ZYkhyy/view?usp=drive_link"}]
            },
            {
                "unit": 2,
                "syllabus": "UNIT - II: Eigen values and Eigen vectors Linear Transformation and Orthogonal Transformation: Eigenvalues, Eigenvectors and their properties, Diagonalization of a matrix, Cayley-Hamilton Theorem (without proof), finding inverse and power of a matrix by Cayley-Hamilton Theorem, Quadratic forms and Nature of the Quadratic Forms, Reduction of Quadratic form to canonical forms by Orthogonal Transformation.",
                "notes": [{"name": "Unit 2 matrices notes", "file_path": "https://drive.google.com/file/d/1CuYQfFLW9dIFMBQU2sHIwrfdFUIB16gh/view?usp=drive_link"}]
            },
            {
                "unit": 3,
                "syllabus": "UNIT - III: Calculus: Mean value theorems: Rolle’s theorem, Lagrange’s Mean value theorem with their Geometrical Interpretation and applications, Cauchy’s Mean value Theorem, Taylor’s Series. Applications of definite integrals to evaluate surface areas and volumes of revolutions of curves (Only in Cartesian coordinates), Definition of Improper Integral: Beta and Gamma functions and their applications.",
                "notes": [{"name": "Unit 3 calculus notes", "file_path": "https://drive.google.com/file/d/1dO0XhTJwzKzDQgUlLeS9NhcVYkCMGQs3/view?usp=drive_link"}]
            },
            {
                "unit": 4,
                "syllabus": "UNIT - IV: Multivariable Calculus (Partial Differentiation and applications): Definitions of Limit and continuity. Partial Differentiation: Euler’s Theorem, Total derivative, Jacobian, Functional dependence & independence. Applications: Maxima and minima of functions of two variables and three variables using method of Lagrange multipliers.",
                "notes": [{"name": "Unit 4 Multivariable Calculus notes", "file_path": "https://drive.google.com/file/d/1BVBAUKpdYn7XgGRe4jZUyo0Yw_IJJBq1/view?usp=drive_link"}]
            },
            {
                "unit": 5,
                "syllabus": "UNIT - V: Multivariable Calculus (Integration): Evaluation of Double Integrals (Cartesian and polar coordinates), change of order of integration (only Cartesian form), Evaluation of Triple Integrals: Change of variables (Cartesian to polar) for double and (Cartesian to Spherical and Cylindrical polar coordinates) for triple integrals. Applications: Areas (by double integrals) and volumes (by double and triple integrals).",
                "notes": [{"name": "Unit 5 Multivariable Calculus notes", "file_path": "https://drive.google.com/file/d/1yUaf2OlOk5rUdTpmrm9YwImD9PIPP4S4/view?usp=drive_link"}]
            }
        ],
        "previous_questions": "https://drive.google.com/file/d/1FYNaT7sGqghSQ8oKipevjPJikWoypFUH/view?usp=drive_link"
    },
    2: {
        "name": "Applied Physics",
        "units": [
            {
                "unit": 1,
                "syllabus": "UNIT - I: QUANTUM PHYSICS AND SOLIDS Quantum Mechanics: Introduction to quantum physics, blackbody radiation – Stefan-Boltzmann’s law, Wein’s and Rayleigh-Jean’s law, Planck’s radiation law - photoelectric effect - Davisson and Germer experiment –Heisenberg uncertainty principle - Born interpretation of the wave function – time independent Schrodinger wave equation - particle in one dimensional potential box. Solids: Symmetry in solids, free electron theory (Drude & Lorentz, Sommerfeld) - Fermi-Dirac distribution - Bloch’s theorem -Kronig-Penney model – E-K diagram- effective mass of electron-origin of energy bands- classification of solids.",
                "notes": [{"name": "Unit 1 QUANTUM PHYSICS AND SOLIDS Notes", "file_path": "https://docs.google.com/presentation/d/1gB4bTeSEUjkOoKLkJCoHQpL6631juIpZ/edit?usp=drive_link&ouid=115691518403405361946&rtpof=true&sd=true"}]
            },
            {
                "unit": 2,
                "syllabus": "UNIT - II: SEMICONDUCTORS AND DEVICES ntrinsic and extrinsic semiconductors – Hall effect - direct and indirect band gap semiconductors - construction, principle of operation and characteristics of P-N Junction diode, Zener diode and bipolar junction transistor (BJT)–LED, PIN diode, avalanche photo diode (APD) and solar cells, their structure, materials, working principle and characteristics.",
                "notes": [{"name": "Unit 2 SEMICONDUCTORS AND DEVICES Notes", "file_path": "https://docs.google.com/presentation/d/1gB4bTeSEUjkOoKLkJCoHQpL6631juIpZ/edit?usp=drive_link&ouid=115691518403405361946&rtpof=true&sd=true"}]
            },
            {
                "unit": 3,
                "syllabus": "UNIT - III: DIELECTRIC, MAGNETIC AND ENERGY MATERIALS Dielectric Materials: Basic definitions- types of polarizations (qualitative) - ferroelectric, piezoelectric, and pyroelectric materials – applications – liquid crystal displays (LCD) and crystal oscillators. Magnetic Materials: Hysteresis - soft and hard magnetic materials - magnetostriction, magnetoresistance - applications - bubble memory devices, magnetic field sensors and multiferroics. Energy Materials: Conductivity of liquid and solid electrolytes- superionic conductors - materials and electrolytes for super capacitors - rechargeable ion batteries, solid fuel cells.",
                "notes": [{"name": "Unit 3 DIELECTRIC, MAGNETIC AND ENERGY MATERIALS Notes", "file_path": "https://docs.google.com/presentation/d/1J7mP-9zqKAs97JxC_hawzvjI5ElUMdGF/edit?usp=drive_link&ouid=115691518403405361946&rtpof=true&sd=true"}]
            },
            {
                "unit": 4,
                "syllabus": "UNIT - IV: NANOTECHNOLOGY Nanoscale, quantum confinement, surface to volume ratio, bottom-up fabrication: sol-gel, precipitation, combustion methods – top-down fabrication: ball milling - physical vapor deposition (PVD) - chemical vapor deposition (CVD) - characterization techniques - XRD, SEM &TEM - applications of nanomaterials.",
                "notes": [{"name": "Unit 4 NANOTECHNOLOGY Nanoscale Notes", "file_path": "https://docs.google.com/presentation/d/147vt_hrMp6DLRmR9TUwMrxbHFyACp75v/edit?usp=drive_link&ouid=115691518403405361946&rtpof=true&sd=true"}]
            },
            {
                "unit": 5,
                "syllabus": "UNIT - V: LASER AND FIBER OPTICS Lasers: Laser beam characteristics-three quantum processes-Einstein coefficients and their relations-lasing action - pumping methods- ruby laser, He-Ne laser , CO2 laser, Argon ion Laser, Nd:YAG laser-semiconductor laser-applications of laser. Fiber Optics: Introduction to optical fiber- advantages of optical Fibers - total internal reflection-construction of optical fiber - acceptance angle - numerical aperture- classification of optical fibers-losses in optical fiber - optical fiber for communication system - applications.",
                "notes": [{"name": "Unit 5 LASER AND FIBER OPTICS Lasers", "file_path": "https://docs.google.com/presentation/d/1vhfPOMCMswqJ8oNjNt0Kr66NqJQurYQc/edit?usp=drive_link&ouid=115691518403405361946&rtpof=true&sd=true"}]
            }
        ],
        "previous_questions": "https://drive.google.com/drive/folders/1vsnODH6FUTmIuS-zFRXdDTU9H3Lfnz7B? usp=drive_link"
    },
    3: {
        "name": "English",
        "units": [
            {
                "unit": 1,
                "syllabus": "UNIT - I Chapter entitled ‘Toasted English’ by R.K.Narayan from “English: Language, Context and Culture” published by Orient BlackSwan, Hyderabad. Vocabulary: The Concept of Word Formation -The Use of Prefixes and Suffixes - Acquaintance with Prefixes and Suffixes from Foreign Languages to form Derivatives - Synonyms and Antonyms. Grammar: Identifying Common Errors in Writing with Reference to Articles and Prepositions. Reading: Reading and Its Importance- Techniques for Effective Reading. Writing: Sentence Structures -Use of Phrases and Clauses in Sentences- Importance of Proper Punctuation- Techniques for Writing precisely – Paragraph Writing – Types, Structures and Features of a Paragraph - Creating Coherence-Organizing Principles of Paragraphs in Documents",
                "notes": [
                    {
                        "name": "Unit 1 Toasted English notes",
                        "file_path": "https://drive.google.com/file/d/13nJYseCLmrBqPCul-6K2cqPJIB07hpEF/view?usp=drive_link"
                    }
                ]
            },
            {
                "unit": 2,
                "syllabus": "UNIT - II Chapter entitled ‘Appro JRD’ by Sudha Murthy from “English: Language, Context and Culture” published by Orient BlackSwan, Hyderabad. Vocabulary: Words Often Misspelt - Homophones, Homonyms and Homographs. Grammar: Identifying Common Errors in Writing with Reference to Noun-pronoun Agreement and Subject-verb Agreement. Reading: Sub-Skills of Reading – Skimming and Scanning – Exercises for Practice. Writing: Nature and Style of Writing- Defining /Describing People, Objects, Places and Events – Classifying- Providing Examples or Evidence.",
                "notes": [
                    {
                        "name": "Unit 2 ‘Appro JRD’ notes",
                        "file_path": "https://drive.google.com/file/d/1VuIRoqq_rCeNhVRh7_Gdqa9cd3el1-mb/view?usp=drive_link"
                    }
                ]
            },
            {
                "unit": 3,
                "syllabus": "UNIT - III Chapter entitled ‘Lessons from Online Learning’ by F.Haider Alvi, Deborah Hurst et al from “English: Language, Context and Culture” published by Orient BlackSwan, Hyderabad. Vocabulary: Words Often Confused - Words from Foreign Languages and their Use in English. Grammar: Identifying Common Errors in Writing with Reference to Misplaced Modifiers and Tenses. Reading: Sub-Skills of Reading – Intensive Reading and Extensive Reading – Exercises for Practice. Writing: Format of a Formal Letter-Writing Formal Letters E.g., Letter of Complaint, Letter of Requisition, Email Etiquette, Job Application with CV/Resume.",
                "notes": [
                    {
                        "name": "Unit 3 ‘Lessons from Online Learning’ Notes",
                        "file_path": "https://drive.google.com/file/d/1tb8xaGL6hEOyekJKJO8E6JNUCzH2YrnU/view?usp=drive_link"
                    }
                ]
            },
            {
                "unit": 4,
                "syllabus": "UNIT - IV Chapter entitled ‘Art and Literature’ by Abdul Kalam from “English: Language, Context and Culture” published by Orient BlackSwan, Hyderabad. Vocabulary: Standard Abbreviations in English. Grammar: Redundancies and Clichés in Oral and Written Communication. Reading: Survey, Question, Read, Recite and Review (SQ3R Method) - Exercises for Practice. Writing: Writing Practices- Essay Writing-Writing Introduction and Conclusion -Précis Writing.",
                "notes": [
                    {
                        "name": "Unit 4 ‘Art and Literature’ notes",
                        "file_path": "https://docs.google.com/presentation/d/1ewuY1gPoFRomjywCgacT1it49b243Ajp/edit?usp=drive_link&ouid=115691518403405361946&rtpof=true&sd=true"
                    }
                ]
            },
            {
                "unit": 5,
                "syllabus": "UNIT - V Chapter entitled ‘Go, Kiss the World’ by Subroto Bagchi from “English: Language, Context and Culture” published by Orient BlackSwan, Hyderabad. Vocabulary: Technical Vocabulary and their Usage. Grammar: Common Errors in English (Covering all the other aspects of grammar which were not covered in the previous units). Reading: Reading Comprehension-Exercises for Practice. Writing: Technical Reports- Introduction – Characteristics of a Report – Categories of Reports Formats- Structure of Reports (Man uscript Format) -Types of Reports - Writing a Report.",
                "notes": [
                    {
                        "name": "Unit 5 ‘Go, Kiss the World’ Notes",
                        "file_path": "https://docs.google.com/presentation/d/124HEm5gCAMj3Tvo15Xzy06vszGtcFJx8/edit?usp=drive_link&ouid=115691518403405361946&rtpof=true&sd=true"
                    }
                ]
            }
        ],
        "previous_questions": "https://docs.google.com/document/d/1NLcmka1vWnS_fD3SGloDGv6MaPUf42bx/edit?usp=drive_link&ouid=115691518403405361946&rtpof=true&sd=true"
    }
}
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/previous_papers')
def previous_papers():
    return render_template('previous_papers.html')

@app.route('/subject', methods=['GET'])
def subject_page():
    subject_id = request.args.get('subject_id', type=int)
    subject = subject_files.get(subject_id)
    if subject is None:
        return "Subject not found!", 404
    return render_template('subject_page.html', subject=subject)

@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/send_email', methods=['POST'])
def send_email():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    # Email configuration
    EMAIL_ADDRESS = "rvarshith68@gmail.com"  # Replace with your email address
    EMAIL_PASSWORD = "jiwb ayia sjyq cjyi"   # Replace with your email password

    # Create the email content
    subject = f"New Contact Form Submission from {name}"
    body = f"Name: {name}\nEmail: {email}\nMessage: {message}"

    # Create email message
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS  # You can also set a different recipient

    # Create a secure SSL context
    context = ssl.create_default_context()

    try:
        # Send the email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)  # Login to your email
            server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.as_string())  # Send the email
        
        # Redirect back to the contact form with a query parameter to show success
        return redirect(url_for('contact', thank_you=True))
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Failed to send email."


if __name__ == '__main__':
    app.run(debug=True)