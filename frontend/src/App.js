import React, { useState, useEffect } from 'react';
import { getData, createData } from './services/api';
import './App.css';

function App() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [newItemName, setNewItemName] = useState('');
  const [selectedFormat, setSelectedFormat] = useState('Détection automatique');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await getData();
      setItems(response.data);
      setLoading(false);
      setError(null);
    } catch (err) {
      setError('Erreur de connexion au backend');
      setLoading(false);
    }
  };

  const handleProcess = async (e) => {
    e.preventDefault();
    if (!newItemName) return alert("Veuillez entrer un nom de salon");
    
    try {
      await createData({ name: newItemName, description: `Format: ${selectedFormat}` });
      setNewItemName('');
      alert('Traitement lancé avec succès');
      fetchData();
    } catch (err) {
      alert('Erreur lors du traitement');
    }
  };

  if (loading) return <div className="loading-screen">Chargement de la plateforme...</div>;

  return (
    <div className="app-wrapper">
      <nav className="navbar">
        <div className="nav-logo">
          <span className="logo-text">CSV CRM Transformer</span>
        </div>
        <div className="nav-actions">
          <button className="nav-btn active">Accueil</button>
          <button className="nav-btn">Administration</button>
          <button className="nav-btn logout">Déconnexion</button>
        </div>
      </nav>

      <main className="container">
        <header className="hero-section">
          <h1>Transformateur CSV CRM</h1>
          <p>Importez et transformez vos fichiers CSV de salons pour le CRM</p>
        </header>

        <div className="main-card">
          <div className="card-header">
            <div className="header-text">
              <h3>Importer un fichier CSV</h3>
              <p>Sélectionnez votre fichier CSV et configurez le traitement</p>
            </div>
          </div>

          <form className="transform-form" onSubmit={handleProcess}>
            <div className="input-group">
              <label>Nom du salon</label>
              <input 
                type="text" 
                placeholder="Ex: Salon de l'Étudiant Paris 2026"
                value={newItemName}
                onChange={(e) => setNewItemName(e.target.value)}
              />
            </div>

            <div className="input-group">
              <label>Format du fichier</label>
              <select 
                value={selectedFormat} 
                onChange={(e) => setSelectedFormat(e.target.value)}
              >
                <option>Détection automatique</option>
                <option>Format Standard</option>
              </select>
            </div>

            <div className="input-group">
              <label>Fichier CSV</label>
              <div className="file-input-custom">
                <button type="button" className="browse-btn">Parcourir...</button>
                <span className="file-name">Aucun fichier sélectionné.</span>
              </div>
            </div>

            <div className="features-highlight">
              <h4>Fonctionnalités automatiques</h4>
              <ul>
                <li>Validation et correction des emails</li>
                <li>Validation et formatage des numéros de téléphone (+33)</li>
                <li>Auto-remplissage de la ville selon le code postal</li>
                <li>Attribution du campus selon la formation</li>
                <li>Calcul de la date de rentrée prévisionnelle</li>
              </ul>
            </div>

            <button type="submit" className="submit-btn">
              Traiter le fichier
            </button>
          </form>
        </div>

        <p className="legal-footer">
          Les fichiers ne sont pas stockés. Vos données sont traitées localement et disparaissent une fois la page fermée.
        </p>
        
        {error && <p className="error-msg">{error}</p>}
      </main>
    </div>
  );
}

export default App;