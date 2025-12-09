import React from 'react';
import './Nash.css';

function NashProblem() {
    return (
        <div className="nash-container">
            <h1>Teoria Jocurilor: Echilibru Nash</h1>
            <div className="placeholder-content">
                <p>⚠️ <strong>În dezvoltare</strong> (Livrabil 3)</p>
                <p>Această componentă va permite:</p>
                <ul>
                    <li>Generarea matricelor de joc în Formă Normală (US-I.2).</li>
                    <li>Identificarea Echilibrului Nash Pur.</li>
                    <li>Verificarea coordonatelor introduse de utilizator.</li>
                </ul>
                <div className="mock-matrix">
                    [ Aici va fi afișată Matricea ]
                </div>
            </div>
        </div>
    );
}

export default NashProblem;