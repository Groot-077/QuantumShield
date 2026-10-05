"""
QuantumShield PowerPoint (.pptx) Generator Script
Generates a 16:9 8-slide Microsoft PowerPoint presentation file (QuantumShield_Presentation.pptx).
"""

import sys
import os

def create_presentation():
    try:
        from pptx import Presentation
        from pptx.util import Inches, Pt
        from pptx.enum.text import PP_ALIGN
        from pptx.dml.color import RGBColor
        from pptx.enum.shapes import MSO_SHAPE
    except ImportError:
        print("INFO: python-pptx is not installed. To generate native .pptx file, run: pip install python-pptx")
        print("Alternative: Open http://127.0.0.1:5000/presentation in your browser to view and export full 16:9 slides!")
        return

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # Color Palette
    COLOR_BG = RGBColor(15, 23, 42)
    COLOR_PRIMARY = RGBColor(2, 132, 199)
    COLOR_TEXT = RGBColor(248, 250, 252)
    COLOR_SUB = RGBColor(203, 213, 225)
    COLOR_CARD = RGBColor(30, 41, 59)

    slides_data = [
        {
            "title": "QuantumShield Framework",
            "subtitle": "A Post-Quantum Secure Password Authentication Framework Using Memory-Hard Hashing and Lattice Cryptography",
            "bullets": [
                "B.Tech Cyber Security Capstone Presentation (2026)",
                "Team Members:",
                "1. Jaipal Prakash (Reg: 23BCE0310)",
                "2. Nikhil Kumar (Reg: 23BCE0404)",
                "3. Ujjawal Kumar (Reg: 23BCE0354)"
            ]
        },
        {
            "title": "Abstract",
            "subtitle": "Executive Summary & Core Solution",
            "bullets": [
                "Quantum Threat: Emerging quantum computers render classical RSA/ECC vulnerable to Shor's algorithm.",
                "Argon2id Memory-Hard Hashing: 64MB memory cost prevents mass GPU/ASIC parallel dictionary cracking.",
                "CRYSTALS-Kyber-512 Integration: NIST PQC standardized lattice cryptography over polynomial ring R_q.",
                "Quantum Commitment (C_q): BLAKE2b digest binding lattice keypair with Argon2id password hash.",
                "Tech Stack: Python Flask, MySQL, HTML5, CSS3, JavaScript, Bootstrap 5."
            ]
        },
        {
            "title": "Problem Statement & Objectives",
            "subtitle": "Threat Model & Goals",
            "bullets": [
                "Problem 1: Grover's Algorithm reduces hash entropy; Shor's Algorithm breaks classical asymmetric encryption.",
                "Problem 2: Classical hashes (SHA-256, MD5) allow billions of parallel dictionary attempts per second on GPUs.",
                "Objective 1: Design memory-hard password authentication using Argon2id.",
                "Objective 2: Integrate CRYSTALS-Kyber-512 Post-Quantum Cryptography into web auth pipeline.",
                "Objective 3: Implement anti-brute-force account lockout (5 failed attempts = 15 min lock) & audit logging."
            ]
        },
        {
            "title": "Literature Survey & Research Gap",
            "subtitle": "Background Study & Innovation",
            "bullets": [
                "Alex Biryukov et al. (Argon2): Introduced Argon2 hashing. Limitation: Lacks PQC protection.",
                "NIST PQC Project: Standardized CRYSTALS-Kyber. Limitation: Focuses on encryption/KEM, not password auth.",
                "Open Quantum Safe (liboqs): C library for PQC primitives. Limitation: Lacks web app integration framework.",
                "Research Gap Addressed: QuantumShield unifies Argon2id memory-hardness and Kyber lattice keys into a single web auth framework."
            ]
        },
        {
            "title": "System Architecture & Execution Flow",
            "subtitle": "Pipeline Overview",
            "bullets": [
                "1. User Registration: Sanitized input -> 16-byte random salt S -> Argon2id Hash (m=64MB, t=3, p=4).",
                "2. Lattice Key Generation: CRYSTALS-Kyber-512 generates Module-LWE public (pk) and secret (sk) keypairs.",
                "3. Quantum Commitment: C_q = BLAKE2b-512(pk || Argon2idHash || Salt) stored in MySQL database.",
                "4. Authentication Verification: Re-verifies Argon2id hash and re-computes C_q in constant time."
            ]
        },
        {
            "title": "Methodology",
            "subtitle": "5-Phase Development Lifecycle",
            "bullets": [
                "Phase 1: Requirement Analysis - Quantum threat modeling and parameter sizing.",
                "Phase 2: Architecture & Database Design - Flask Blueprint MVC & MySQL ER schema.",
                "Phase 3: Core Development - Argon2id, Kyber-512 engine, Flask backend, Bootstrap UI.",
                "Phase 4: Security Testing - Account lockout verification, SQLi/XSS prevention, CSRF validation.",
                "Phase 5: Local Deployment - Server deployment on localhost:5000."
            ]
        },
        {
            "title": "Expected Results & Key Deliverables",
            "subtitle": "System Verification & Backward Capabilities",
            "bullets": [
                "✔ Memory-Hard GPU Immunity: 64MB RAM parameter blocks parallel dictionary cracking.",
                "✔ Quantum Commitment Verification: Zero-knowledge style verification matching C_q digest.",
                "✔ Backward Secrecy (Post-Compromise Security): Periodic Kyber-512 key ratcheting revokes past compromised material.",
                "✔ Backward Compatibility: Seamless fallback and automatic migration from legacy hashes (werkzeug/pbkdf2/sha256) to Argon2id.",
                "✔ Admin SOC Dashboard: Live Chart.js analytics graph, user lock/unlock controls, and IP audit trail."
            ]
        },
        {
            "title": "Conclusion & Future Scope",
            "subtitle": "Summary & Industry Roadmap",
            "bullets": [
                "Conclusion: QuantumShield provides a practical, scalable post-quantum authentication framework.",
                "Future Scope 1: CRYSTALS-Dilithium digital signature integration for JWT session tokens.",
                "Future Scope 2: Hardware Security Module (HSM / TPM) isolation for private lattice key storage.",
                "Future Scope 3: FIDO2 / WebAuthn biometric post-quantum extensions."
            ]
        }
    ]

    for slide_info in slides_data:
        slide = prs.slides.add_slide(blank_layout)

        # Background
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = COLOR_BG
        bg.line.fill.background()

        # Title Box
        tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(11.7), Inches(1.2))
        tf = tx_box.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = slide_info["subtitle"].upper()
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = COLOR_PRIMARY

        p2 = tf.add_paragraph()
        p2.text = slide_info["title"]
        p2.font.size = Pt(28)
        p2.font.bold = True
        p2.font.color.rgb = COLOR_TEXT

        # Content Card
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.0), Inches(11.7), Inches(4.8))
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_CARD
        card.line.color.rgb = COLOR_PRIMARY

        c_tf = card.text_frame
        c_tf.word_wrap = True
        c_tf.margin_left = Inches(0.4)
        c_tf.margin_top = Inches(0.4)

        for i, bullet in enumerate(slide_info["bullets"]):
            bp = c_tf.paragraphs[0] if i == 0 else c_tf.add_paragraph()
            bp.text = bullet
            bp.font.size = Pt(16)
            bp.font.color.rgb = COLOR_SUB
            bp.space_after = Pt(12)

    output_path = "QuantumShield_Presentation.pptx"
    prs.save(output_path)
    print(f"SUCCESS: PowerPoint presentation saved as '{os.path.abspath(output_path)}'")

if __name__ == '__main__':
    create_presentation()
