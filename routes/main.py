"""
Main Blueprint - Public Landing & Educational Routes
Renders project overview, cryptographic framework features, post-quantum technical details, and PPT slide deck.
"""

from flask import Blueprint, render_template
from crypto.kyber import kyber_engine

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home Page - QuantumShield Framework Overview"""
    pqc_info = kyber_engine.get_status_info()
    return render_template('index.html', pqc_info=pqc_info)

@main_bp.route('/pqc-overview')
def pqc_overview():
    """Post-Quantum Cryptography & Argon2id In-depth Explanation Page"""
    pqc_info = kyber_engine.get_status_info()
    return render_template('pqc_overview.html', pqc_info=pqc_info)

@main_bp.route('/architecture')
def architecture():
    """System Architecture & Flowchart Documentation View"""
    return render_template('architecture.html')

@main_bp.route('/presentation')
def presentation():
    """Interactive PowerPoint Presentation Slide Deck View"""
    return render_template('presentation.html')
