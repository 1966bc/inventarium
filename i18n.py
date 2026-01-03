# -*- coding: utf-8 -*-
"""
Internationalization Module for Inventarium.

Provides translation support for Italian, English, Spanish, German and French.

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""

# Available languages
LANGUAGES = {
    "it": "Italiano",
    "en": "English",
    "es": "Español",
    "de": "Deutsch",
    "fr": "Français"
}

# Default language
DEFAULT_LANGUAGE = "it"

# Translation dictionary
TRANSLATIONS = {
    # ==========================================================================
    # Menu - File
    # ==========================================================================
    "File": {"it": "File", "en": "File", "es": "Archivo", "de": "Datei", "fr": "Fichier"},
    "Impostazioni": {"it": "Impostazioni", "en": "Settings", "es": "Configuración", "de": "Einstellungen", "fr": "Paramètres"},
    "Configura Database": {"it": "Configura Database", "en": "Configure Database", "es": "Configurar Base de Datos", "de": "Datenbank konfigurieren", "fr": "Configurer la base de données"},
    "Database": {"it": "Database", "en": "Database", "es": "Base de Datos", "de": "Datenbank", "fr": "Base de données"},
    "Configura": {"it": "Configura", "en": "Configure", "es": "Configurar", "de": "Konfigurieren", "fr": "Configurer"},
    "Backup": {"it": "Backup", "en": "Backup", "es": "Copia de Seguridad", "de": "Sicherung", "fr": "Sauvegarde"},
    "Salva Backup Database": {"it": "Salva Backup Database", "en": "Save Database Backup", "es": "Guardar Copia de Seguridad", "de": "Datenbanksicherung speichern", "fr": "Enregistrer la sauvegarde"},
    "Backup completato!": {"it": "Backup completato!", "en": "Backup completed!", "es": "¡Copia de seguridad completada!", "de": "Sicherung abgeschlossen!", "fr": "Sauvegarde terminée !"},
    "Errore durante il backup:": {"it": "Errore durante il backup:", "en": "Error during backup:", "es": "Error durante la copia de seguridad:", "de": "Fehler bei der Sicherung:", "fr": "Erreur lors de la sauvegarde :"},
    "Compatta": {"it": "Compatta", "en": "Compact", "es": "Compactar", "de": "Komprimieren", "fr": "Compacter"},
    "Backup Database": {"it": "Backup Database", "en": "Backup Database", "es": "Copia de Seguridad", "de": "Datenbank sichern", "fr": "Sauvegarder la base de données"},
    "Compatta Database": {"it": "Compatta Database", "en": "Compact Database", "es": "Compactar Base de Datos", "de": "Datenbank komprimieren", "fr": "Compacter la base de données"},
    "Database compattato!": {"it": "Database compattato!", "en": "Database compacted!", "es": "¡Base de datos compactada!", "de": "Datenbank komprimiert!", "fr": "Base de données compactée !"},
    "Prima": {"it": "Prima", "en": "Before", "es": "Antes", "de": "Vorher", "fr": "Avant"},
    "Dopo": {"it": "Dopo", "en": "After", "es": "Después", "de": "Nachher", "fr": "Après"},
    "Risparmiato": {"it": "Risparmiato", "en": "Saved", "es": "Ahorrado", "de": "Gespart", "fr": "Économisé"},
    "Errore durante la compattazione": {"it": "Errore durante la compattazione", "en": "Error during compaction", "es": "Error durante la compactación", "de": "Fehler beim Komprimieren", "fr": "Erreur lors du compactage"},
    "Configurazione Database": {"it": "Configurazione Database", "en": "Database Configuration", "es": "Configuración de Base de Datos", "de": "Datenbankkonfiguration", "fr": "Configuration de la base de données"},
    "Configura Percorso Database": {"it": "Configura Percorso Database", "en": "Configure Database Path", "es": "Configurar Ruta de Base de Datos", "de": "Datenbankpfad konfigurieren", "fr": "Configurer le chemin de la base de données"},
    "Configurazione del percorso database.": {"it": "Configurazione del percorso database.", "en": "Database path configuration.", "es": "Configuración de la ruta de base de datos.", "de": "Datenbankpfad-Konfiguration.", "fr": "Configuration du chemin de la base de données."},
    "Selezionare il file database SQLite (.db)": {"it": "Selezionare il file database SQLite (.db)", "en": "Select the SQLite database file (.db)", "es": "Seleccione el archivo de base de datos SQLite (.db)", "de": "SQLite-Datenbankdatei (.db) auswählen", "fr": "Sélectionnez le fichier de base de données SQLite (.db)"},
    "o inserire manualmente il percorso.": {"it": "o inserire manualmente il percorso.", "en": "or enter the path manually.", "es": "o ingrese la ruta manualmente.", "de": "oder den Pfad manuell eingeben.", "fr": "ou entrez le chemin manuellement."},
    "Percorso:": {"it": "Percorso:", "en": "Path:", "es": "Ruta:", "de": "Pfad:", "fr": "Chemin :"},
    "Sfoglia...": {"it": "Sfoglia...", "en": "Browse...", "es": "Examinar...", "de": "Durchsuchen...", "fr": "Parcourir..."},
    "Test Connessione": {"it": "Test Connessione", "en": "Test Connection", "es": "Probar Conexión", "de": "Verbindung testen", "fr": "Tester la connexion"},
    "OK": {"it": "OK", "en": "OK", "es": "Aceptar", "de": "OK", "fr": "OK"},
    "Inserire un percorso": {"it": "Inserire un percorso", "en": "Enter a path", "es": "Ingrese una ruta", "de": "Pfad eingeben", "fr": "Entrez un chemin"},
    "File non trovato": {"it": "File non trovato", "en": "File not found", "es": "Archivo no encontrado", "de": "Datei nicht gefunden", "fr": "Fichier non trouvé"},
    "Database non valido": {"it": "Database non valido", "en": "Invalid database", "es": "Base de datos no válida", "de": "Ungültige Datenbank", "fr": "Base de données invalide"},
    "prodotti trovati": {"it": "prodotti trovati", "en": "products found", "es": "productos encontrados", "de": "Produkte gefunden", "fr": "produits trouvés"},
    "Errore": {"it": "Errore", "en": "Error", "es": "Error", "de": "Fehler", "fr": "Erreur"},
    "Seleziona Database": {"it": "Seleziona Database", "en": "Select Database", "es": "Seleccionar Base de Datos", "de": "Datenbank auswählen", "fr": "Sélectionner la base de données"},
    "Tutti i file": {"it": "Tutti i file", "en": "All files", "es": "Todos los archivos", "de": "Alle Dateien", "fr": "Tous les fichiers"},
    "Configurazione": {"it": "Configurazione", "en": "Configuration", "es": "Configuración", "de": "Konfiguration", "fr": "Configuration"},
    "Inserire un percorso valido.": {"it": "Inserire un percorso valido.", "en": "Enter a valid path.", "es": "Ingrese una ruta válida.", "de": "Gültigen Pfad eingeben.", "fr": "Entrez un chemin valide."},
    "Il file non esiste:": {"it": "Il file non esiste:", "en": "File does not exist:", "es": "El archivo no existe:", "de": "Datei existiert nicht:", "fr": "Le fichier n'existe pas :"},
    "Continuare comunque?": {"it": "Continuare comunque?", "en": "Continue anyway?", "es": "¿Continuar de todos modos?", "de": "Trotzdem fortfahren?", "fr": "Continuer quand même ?"},
    "Percorso database aggiornato.": {"it": "Percorso database aggiornato.", "en": "Database path updated.", "es": "Ruta de base de datos actualizada.", "de": "Datenbankpfad aktualisiert.", "fr": "Chemin de la base de données mis à jour."},
    "Riavviare l'applicazione per utilizzare il nuovo database.": {"it": "Riavviare l'applicazione per utilizzare il nuovo database.", "en": "Restart the application to use the new database.", "es": "Reinicie la aplicación para usar la nueva base de datos.", "de": "Anwendung neu starten, um die neue Datenbank zu verwenden.", "fr": "Redémarrez l'application pour utiliser la nouvelle base de données."},
    "Riavviare ora?": {"it": "Riavviare ora?", "en": "Restart now?", "es": "¿Reiniciar ahora?", "de": "Jetzt neu starten?", "fr": "Redémarrer maintenant ?"},
    "Database non trovato.": {"it": "Database non trovato.", "en": "Database not found.", "es": "Base de datos no encontrada.", "de": "Datenbank nicht gefunden.", "fr": "Base de données non trouvée."},
    "Cosa vuoi fare?": {"it": "Cosa vuoi fare?", "en": "What do you want to do?", "es": "¿Qué quieres hacer?", "de": "Was möchten Sie tun?", "fr": "Que voulez-vous faire ?"},
    "Cerca database esistente...": {"it": "Cerca database esistente...", "en": "Find existing database...", "es": "Buscar base de datos existente...", "de": "Vorhandene Datenbank suchen...", "fr": "Rechercher une base de données existante..."},
    "Crea nuovo database": {"it": "Crea nuovo database", "en": "Create new database", "es": "Crear nueva base de datos", "de": "Neue Datenbank erstellen", "fr": "Créer une nouvelle base de données"},
    "Crea Nuovo Database": {"it": "Crea Nuovo Database", "en": "Create New Database", "es": "Crear Nueva Base de Datos", "de": "Neue Datenbank erstellen", "fr": "Créer une nouvelle base de données"},
    "Database Creato": {"it": "Database Creato", "en": "Database Created", "es": "Base de Datos Creada", "de": "Datenbank erstellt", "fr": "Base de données créée"},
    "Database creato con successo!": {"it": "Database creato con successo!", "en": "Database created successfully!", "es": "¡Base de datos creada con éxito!", "de": "Datenbank erfolgreich erstellt!", "fr": "Base de données créée avec succès !"},
    "Impossibile creare il database.": {"it": "Impossibile creare il database.", "en": "Unable to create database.", "es": "No se puede crear la base de datos.", "de": "Datenbank kann nicht erstellt werden.", "fr": "Impossible de créer la base de données."},
    "Il file selezionato non è un database Inventarium valido.": {"it": "Il file selezionato non è un database Inventarium valido.", "en": "The selected file is not a valid Inventarium database.", "es": "El archivo seleccionado no es una base de datos Inventarium válida.", "de": "Die ausgewählte Datei ist keine gültige Inventarium-Datenbank.", "fr": "Le fichier sélectionné n'est pas une base de données Inventarium valide."},
    "File init.sql non trovato!": {"it": "File init.sql non trovato!", "en": "File init.sql not found!", "es": "¡Archivo init.sql no encontrado!", "de": "Datei init.sql nicht gefunden!", "fr": "Fichier init.sql non trouvé !"},
    "Errore durante la creazione del database:": {"it": "Errore durante la creazione del database:", "en": "Error creating database:", "es": "Error al crear la base de datos:", "de": "Fehler beim Erstellen der Datenbank:", "fr": "Erreur lors de la création de la base de données :"},
    "Log": {"it": "Log", "en": "Log", "es": "Registro", "de": "Protokoll", "fr": "Journal"},
    "Etichetta Personalizzata": {"it": "Etichetta Personalizzata", "en": "Custom Label", "es": "Etiqueta Personalizada", "de": "Benutzerdefiniertes Etikett", "fr": "Étiquette personnalisée"},
    "Esci": {"it": "Esci", "en": "Exit", "es": "Salir", "de": "Beenden", "fr": "Quitter"},
    "Lingua": {"it": "Lingua", "en": "Language", "es": "Idioma", "de": "Sprache", "fr": "Langue"},

    # ==========================================================================
    # Menu - Warehouse
    # ==========================================================================
    "Magazzino": {"it": "Magazzino", "en": "Warehouse", "es": "Almacén", "de": "Lager", "fr": "Entrepôt"},
    "Giacenze": {"it": "Giacenze", "en": "Stock", "es": "Existencias", "de": "Bestand", "fr": "Stock"},
    "Stampa Giacenze": {"it": "Stampa Giacenze", "en": "Print Stock", "es": "Imprimir Existencias", "de": "Bestand drucken", "fr": "Imprimer le stock"},
    "Scarico": {"it": "Scarico", "en": "Unload", "es": "Descarga", "de": "Entladen", "fr": "Décharger"},
    "Scadenze": {"it": "Scadenze", "en": "Expiring", "es": "Caducidades", "de": "Ablaufend", "fr": "Expirations"},

    # ==========================================================================
    # Menu - Requests
    # ==========================================================================
    "Richieste": {"it": "Richieste", "en": "Requests", "es": "Solicitudes", "de": "Anfragen", "fr": "Demandes"},
    "Consegne": {"it": "Consegne", "en": "Deliveries", "es": "Entregas", "de": "Lieferungen", "fr": "Livraisons"},

    # ==========================================================================
    # Menu - Admin
    # ==========================================================================
    "Anagrafiche": {"it": "Anagrafiche", "en": "Master Data", "es": "Datos Maestros", "de": "Stammdaten", "fr": "Données de base"},
    "Prodotti": {"it": "Prodotti", "en": "Products", "es": "Productos", "de": "Produkte", "fr": "Produits"},
    "Fornitori": {"it": "Fornitori", "en": "Suppliers", "es": "Proveedores", "de": "Lieferanten", "fr": "Fournisseurs"},
    "Categorie": {"it": "Categorie", "en": "Categories", "es": "Categorías", "de": "Kategorien", "fr": "Catégories"},
    "Conservazioni": {"it": "Conservazioni", "en": "Storage Conditions", "es": "Condiciones de Almacenamiento", "de": "Lagerbedingungen", "fr": "Conditions de stockage"},
    "Ubicazioni": {"it": "Ubicazioni", "en": "Locations", "es": "Ubicaciones", "de": "Standorte", "fr": "Emplacements"},
    "Fonti Finanziamento": {"it": "Fonti Finanziamento", "en": "Funding Sources", "es": "Fuentes de Financiación", "de": "Finanzierungsquellen", "fr": "Sources de financement"},
    "Fonti di Finanziamento": {"it": "Fonti di Finanziamento", "en": "Funding Sources", "es": "Fuentes de Financiación", "de": "Finanzierungsquellen", "fr": "Sources de financement"},
    "Totale": {"it": "Totale", "en": "Total", "es": "Total", "de": "Gesamt", "fr": "Total"},

    # ==========================================================================
    # Menu - Statistics
    # ==========================================================================
    "Statistiche": {"it": "Statistiche", "en": "Statistics", "es": "Estadísticas", "de": "Statistiken", "fr": "Statistiques"},
    "Dashboard": {"it": "Dashboard", "en": "Dashboard", "es": "Panel de Control", "de": "Dashboard", "fr": "Tableau de bord"},
    "Consumi": {"it": "Consumi", "en": "Consumption", "es": "Consumos", "de": "Verbrauch", "fr": "Consommation"},
    "Rotazione": {"it": "Rotazione", "en": "Rotation", "es": "Rotación", "de": "Rotation", "fr": "Rotation"},
    "Tempi (TAT)": {"it": "Tempi (TAT)", "en": "Times (TAT)", "es": "Tiempos (TAT)", "de": "Zeiten (TAT)", "fr": "Délais (TAT)"},

    # ==========================================================================
    # Menu - Help
    # ==========================================================================
    "Informazioni": {"it": "Informazioni", "en": "About", "es": "Acerca de", "de": "Über", "fr": "À propos"},
    "Licenza": {"it": "Licenza", "en": "License", "es": "Licencia", "de": "Lizenz", "fr": "Licence"},
    "Versione Python": {"it": "Versione Python", "en": "Python Version", "es": "Versión de Python", "de": "Python-Version", "fr": "Version Python"},
    "Versione Tkinter": {"it": "Versione Tkinter", "en": "Tkinter Version", "es": "Versión de Tkinter", "de": "Tkinter-Version", "fr": "Version Tkinter"},

    # ==========================================================================
    # Common buttons
    # ==========================================================================
    "Salva": {"it": "Salva", "en": "Save", "es": "Guardar", "de": "Speichern", "fr": "Enregistrer"},
    "Chiudi": {"it": "Chiudi", "en": "Close", "es": "Cerrar", "de": "Schließen", "fr": "Fermer"},
    "Annulla": {"it": "Annulla", "en": "Cancel", "es": "Cancelar", "de": "Abbrechen", "fr": "Annuler"},
    "Nuovo": {"it": "Nuovo", "en": "New", "es": "Nuevo", "de": "Neu", "fr": "Nouveau"},
    "Modifica": {"it": "Modifica", "en": "Edit", "es": "Editar", "de": "Bearbeiten", "fr": "Modifier"},
    "Elimina": {"it": "Elimina", "en": "Delete", "es": "Eliminar", "de": "Löschen", "fr": "Supprimer"},
    "Cerca": {"it": "Cerca", "en": "Search", "es": "Buscar", "de": "Suchen", "fr": "Rechercher"},
    "Aggiorna": {"it": "Aggiorna", "en": "Refresh", "es": "Actualizar", "de": "Aktualisieren", "fr": "Actualiser"},
    "Stampa": {"it": "Stampa", "en": "Print", "es": "Imprimir", "de": "Drucken", "fr": "Imprimer"},
    "Esporta CSV": {"it": "Esporta CSV", "en": "Export CSV", "es": "Exportar CSV", "de": "CSV exportieren", "fr": "Exporter CSV"},
    "Scarica": {"it": "Scarica", "en": "Unload", "es": "Descargar", "de": "Entladen", "fr": "Décharger"},
    "Annulla Lotto": {"it": "Annulla Lotto", "en": "Cancel Batch", "es": "Cancelar Lote", "de": "Charge stornieren", "fr": "Annuler le lot"},
    "Calcola": {"it": "Calcola", "en": "Calculate", "es": "Calcular", "de": "Berechnen", "fr": "Calculer"},
    "Carica": {"it": "Carica", "en": "Load", "es": "Cargar", "de": "Laden", "fr": "Charger"},
    "Anteprima": {"it": "Anteprima", "en": "Preview", "es": "Vista Previa", "de": "Vorschau", "fr": "Aperçu"},
    "Dettagli": {"it": "Dettagli", "en": "Details", "es": "Detalles", "de": "Details", "fr": "Détails"},
    "Storico": {"it": "Storico", "en": "History", "es": "Historial", "de": "Verlauf", "fr": "Historique"},
    "Nuovo Lotto": {"it": "Nuovo Lotto", "en": "New Batch", "es": "Nuevo Lote", "de": "Neue Charge", "fr": "Nouveau lot"},
    "Carica Etichette": {"it": "Carica Etichette", "en": "Load Labels", "es": "Cargar Etiquetas", "de": "Etiketten laden", "fr": "Charger les étiquettes"},
    "Confezioni": {"it": "Confezioni", "en": "Packages", "es": "Envases", "de": "Packungen", "fr": "Conditionnements"},
    "Genera": {"it": "Genera", "en": "Generate", "es": "Generar", "de": "Generieren", "fr": "Générer"},

    # ==========================================================================
    # Package History
    # ==========================================================================
    "Storico Ordini": {"it": "Storico Ordini", "en": "Order History", "es": "Historial de Pedidos", "de": "Bestellverlauf", "fr": "Historique des commandes"},
    "Data": {"it": "Data", "en": "Date", "es": "Fecha", "de": "Datum", "fr": "Date"},
    "Rif. Richiesta": {"it": "Rif. Richiesta", "en": "Request Ref.", "es": "Ref. Solicitud", "de": "Anfrage-Ref.", "fr": "Réf. demande"},
    "Ord.": {"it": "Ord.", "en": "Ord.", "es": "Ped.", "de": "Best.", "fr": "Com."},
    "Evaso": {"it": "Evaso", "en": "Deliv.", "es": "Entr.", "de": "Lief.", "fr": "Livré"},
    "Righe": {"it": "Righe", "en": "Rows", "es": "Filas", "de": "Zeilen", "fr": "Lignes"},
    "Tot. Ord": {"it": "Tot. Ord", "en": "Tot. Ord", "es": "Tot. Ped", "de": "Ges. Best.", "fr": "Tot. Com."},
    "Tot. Evaso": {"it": "Tot. Evaso", "en": "Tot. Deliv", "es": "Tot. Entr", "de": "Ges. Lief.", "fr": "Tot. Livré"},

    # ==========================================================================
    # Batch Dialog
    # ==========================================================================
    "Modifica Lotto": {"it": "Modifica Lotto", "en": "Edit Batch", "es": "Editar Lote", "de": "Charge bearbeiten", "fr": "Modifier le lot"},
    "La data Scadenza non è valida!": {"it": "La data Scadenza non è valida!", "en": "The Expiration date is not valid!", "es": "¡La fecha de Vencimiento no es válida!", "de": "Das Ablaufdatum ist ungültig!", "fr": "La date d'expiration n'est pas valide !"},
    "Il lotto '{}' con scadenza {} esiste già!": {"it": "Il lotto '{}' con scadenza {} esiste già!", "en": "Batch '{}' with expiration {} already exists!", "es": "¡El lote '{}' con vencimiento {} ya existe!", "de": "Charge '{}' mit Ablauf {} existiert bereits!", "fr": "Le lot '{}' avec expiration {} existe déjà !"},
    "Il lotto '{}' esiste già con scadenza {}.\nVuoi inserirlo comunque con scadenza {}?": {"it": "Il lotto '{}' esiste già con scadenza {}.\nVuoi inserirlo comunque con scadenza {}?", "en": "Batch '{}' already exists with expiration {}.\nInsert anyway with expiration {}?", "es": "El lote '{}' ya existe con vencimiento {}.\n¿Insertar de todos modos con vencimiento {}?", "de": "Batch '{}' already exists with expiration {}.\\nInsert anyway with expiration {}?", "fr": "Batch '{}' already exists with expiration {}.\\nInsert anyway with expiration {}?"},
    "Il lotto è già scaduto!\nImpossibile inserire.": {"it": "Il lotto è già scaduto!\nImpossibile inserire.", "en": "The batch is already expired!\nCannot insert.", "es": "¡El lote ya está vencido!\nNo se puede insertar.", "de": "The batch is already expired!\\nCannot insert.", "fr": "The batch is already expired!\\nCannot insert."},
    "Attenzione: il lotto scade tra {} giorni.\nProcedere comunque?": {"it": "Attenzione: il lotto scade tra {} giorni.\nProcedere comunque?", "en": "Warning: batch expires in {} days.\nProceed anyway?", "es": "Advertencia: el lote vence en {} días.\n¿Continuar de todos modos?", "de": "Warning: batch expires in {} days.\\nProceed anyway?", "fr": "Warning: batch expires in {} days.\\nProceed anyway?"},

    # ==========================================================================
    # Custom Label
    # ==========================================================================
    "Riga 1:": {"it": "Riga 1:", "en": "Line 1:", "es": "Línea 1:", "de": "Zeile 1:", "fr": "Ligne 1 :"},
    "Riga 2:": {"it": "Riga 2:", "en": "Line 2:", "es": "Línea 2:", "de": "Zeile 2:", "fr": "Ligne 2 :"},
    "Riga 3:": {"it": "Riga 3:", "en": "Line 3:", "es": "Línea 3:", "de": "Zeile 3:", "fr": "Ligne 3 :"},
    "Dim. Font:": {"it": "Dim. Font:", "en": "Font Size:", "es": "Tam. Fuente:", "de": "Schriftgröße:", "fr": "Taille police :"},
    "Etichetta Personalizzata": {"it": "Etichetta Personalizzata", "en": "Custom Label", "es": "Etiqueta Personalizada", "de": "Benutzerdefiniertes Etikett", "fr": "Étiquette personnalisée"},
    "Errore nel salvare i modelli:": {"it": "Errore nel salvare i modelli:", "en": "Error saving templates:", "es": "Error al guardar plantillas:", "de": "Fehler beim Speichern der Vorlagen:", "fr": "Erreur lors de l'enregistrement des modèles :"},
    "Inserire almeno la prima riga!": {"it": "Inserire almeno la prima riga!", "en": "Enter at least the first line!", "es": "¡Ingrese al menos la primera línea!", "de": "Mindestens die erste Zeile eingeben!", "fr": "Entrez au moins la première ligne !"},
    "Il modello '{}' esiste.\nSovrascrivere?": {"it": "Il modello '{}' esiste.\nSovrascrivere?", "en": "Template '{}' exists.\nOverwrite?", "es": "La plantilla '{}' existe.\n¿Sobrescribir?", "de": "Template '{}' exists.\\nOverwrite?", "fr": "Template '{}' exists.\\nOverwrite?"},
    "Modello '{}' salvato!": {"it": "Modello '{}' salvato!", "en": "Template '{}' saved!", "es": "¡Plantilla '{}' guardada!", "de": "Vorlage '{}' gespeichert!", "fr": "Modèle '{}' enregistré !"},
    "Eliminare il modello '{}'?": {"it": "Eliminare il modello '{}'?", "en": "Delete template '{}'?", "es": "¿Eliminar plantilla '{}'?", "de": "Vorlage '{}' löschen?", "fr": "Supprimer le modèle '{}' ?"},
    "Inserire almeno una riga di testo!": {"it": "Inserire almeno una riga di testo!", "en": "Enter at least one line of text!", "es": "¡Ingrese al menos una línea de texto!", "de": "Mindestens eine Textzeile eingeben!", "fr": "Entrez au moins une ligne de texte !"},
    "Errore nella generazione:": {"it": "Errore nella generazione:", "en": "Error in generation:", "es": "Error en la generación:", "de": "Fehler bei der Generierung:", "fr": "Erreur lors de la génération :"},
    "Etichetta inviata alla stampa!": {"it": "Etichetta inviata alla stampa!", "en": "Label sent to print!", "es": "¡Etiqueta enviada a imprimir!", "de": "Etikett zum Drucken gesendet!", "fr": "Étiquette envoyée à l'impression !"},
    "Errore nella stampa:": {"it": "Errore nella stampa:", "en": "Error in printing:", "es": "Error en la impresión:", "de": "Fehler beim Drucken:", "fr": "Erreur lors de l'impression :"},

    # ==========================================================================
    # Expiring Batches
    # ==========================================================================
    "GG Scad.": {"it": "GG Scad.", "en": "Days Exp.", "es": "Días Venc.", "de": "Tage Abl.", "fr": "Jours Exp."},
    "Giac.": {"it": "Giac.", "en": "Stock", "es": "Stock", "de": "Bestand", "fr": "Stock"},
    "Lotti in Scadenza (30 giorni)": {"it": "Lotti in Scadenza (30 giorni)", "en": "Expiring Batches (30 days)", "es": "Lotes por Vencer (30 días)", "de": "Ablaufende Chargen (30 Tage)", "fr": "Lots expirants (30 jours)"},
    "GG Rim.": {"it": "GG Rim.", "en": "Days Left", "es": "Días Rest.", "de": "Tage übrig", "fr": "Jours rest."},
    "Seleziona un lotto scaduto da annullare!": {"it": "Seleziona un lotto scaduto da annullare!", "en": "Select an expired batch to cancel!", "es": "¡Seleccione un lote vencido para cancelar!", "de": "Abgelaufene Charge zum Stornieren auswählen!", "fr": "Sélectionnez un lot expiré à annuler !"},
    "Annullare il lotto '{}' di '{}'?\n\nVerranno annullate {} etichette in giacenza.\n\nQuesta operazione non è reversibile.": {"it": "Annullare il lotto '{}' di '{}'?\n\nVerranno annullate {} etichette in giacenza.\n\nQuesta operazione non è reversibile.", "en": "Cancel batch '{}' of '{}'?\n\n{} labels in stock will be cancelled.\n\nThis operation is not reversible.", "es": "¿Cancelar lote '{}' de '{}'?\n\nSe cancelarán {} etiquetas en stock.\n\nEsta operación no es reversible.", "de": "Cancel batch '{}' of '{}'?\\n\\n{} labels in stock will be cancelled.\\n\\nThis operation is not reversible.", "fr": "Cancel batch '{}' of '{}'?\\n\\n{} labels in stock will be cancelled.\\n\\nThis operation is not reversible."},
    "Lotto '{}' annullato con successo.": {"it": "Lotto '{}' annullato con successo.", "en": "Batch '{}' cancelled successfully.", "es": "Lote '{}' cancelado exitosamente.", "de": "Charge '{}' erfolgreich storniert.", "fr": "Lot '{}' annulé avec succès."},

    # ==========================================================================
    # Labels Dialog
    # ==========================================================================
    "Prodotto:": {"it": "Prodotto:", "en": "Product:", "es": "Producto:", "de": "Produkt:", "fr": "Produit :"},
    "Numero etichette:": {"it": "Numero etichette:", "en": "Number of labels:", "es": "Número de etiquetas:", "de": "Anzahl Etiketten:", "fr": "Nombre d'étiquettes :"},
    "Inserire un numero di etichette valido!": {"it": "Inserire un numero di etichette valido!", "en": "Enter a valid number of labels!", "es": "¡Ingrese un número de etiquetas válido!", "de": "Gültige Anzahl Etiketten eingeben!", "fr": "Entrez un nombre d'étiquettes valide !"},
    "Caricare {} etichetta?": {"it": "Caricare {} etichetta?", "en": "Load {} label?", "es": "¿Cargar {} etiqueta?", "de": "{} Etikett laden?", "fr": "Charger {} étiquette ?"},
    "Caricare {} etichette?": {"it": "Caricare {} etichette?", "en": "Load {} labels?", "es": "¿Cargar {} etiquetas?", "de": "{} Etiketten laden?", "fr": "Charger {} étiquettes ?"},

    # ==========================================================================
    # Locations
    # ==========================================================================
    "Tipo:": {"it": "Tipo:", "en": "Type:", "es": "Tipo:", "de": "Typ:", "fr": "Type :"},
    "-- Non assegnato --": {"it": "-- Non assegnato --", "en": "-- Not assigned --", "es": "-- No asignado --", "de": "-- Nicht zugewiesen --", "fr": "-- Non assigné --"},
    "Stanza": {"it": "Stanza", "en": "Room", "es": "Sala", "de": "Raum", "fr": "Salle"},
    "Conserv.": {"it": "Conserv.", "en": "Storage", "es": "Conserv.", "de": "Lagerung", "fr": "Stockage"},
    "Seleziona ubicazione:": {"it": "Seleziona ubicazione:", "en": "Select location:", "es": "Seleccionar ubicación:", "de": "Standort auswählen:", "fr": "Sélectionner l'emplacement :"},

    # ==========================================================================
    # Packages
    # ==========================================================================
    "Cod.Forn.": {"it": "Cod.Forn.", "en": "Suppl.Code", "es": "Cód.Prov.", "de": "Lief.Code", "fr": "Code fourn."},
    "Et.": {"it": "Et.", "en": "Lab.", "es": "Et.", "de": "Et.", "fr": "Ét."},
    "B": {"it": "B", "en": "D", "es": "O", "de": "D", "fr": "O"},

    # ==========================================================================
    # Report Fundings
    # ==========================================================================
    "In Gara:": {"it": "In Gara:", "en": "Tender:", "es": "Licitación:", "de": "Ausschreibung:", "fr": "Appel d'offres :"},
    "Economia:": {"it": "Economia:", "en": "Budget:", "es": "Presupuesto:", "de": "Budget:", "fr": "Budget :"},

    # ==========================================================================
    # Requests
    # ==========================================================================
    "Art.": {"it": "Art.", "en": "It.", "es": "Art.", "de": "Art.", "fr": "Art."},
    "Conf.": {"it": "Conf.", "en": "Pack.", "es": "Conf.", "de": "Pack.", "fr": "Cond."},
    "Qtà": {"it": "Qtà", "en": "Qty", "es": "Cant.", "de": "Menge", "fr": "Qté"},

    # ==========================================================================
    # Warehouse
    # ==========================================================================
    "G.": {"it": "G.", "en": "S.", "es": "S.", "de": "B.", "fr": "S."},
    "GG": {"it": "GG", "en": "Days", "es": "Días", "de": "Tage", "fr": "Jours"},

    # ==========================================================================
    # Statistics
    # ==========================================================================
    "Perdita %": {"it": "Perdita %", "en": "Loss %", "es": "Pérdida %", "de": "Verlust %", "fr": "Perte %"},
    "Efficienza %": {"it": "Efficienza %", "en": "Efficiency %", "es": "Eficiencia %", "de": "Effizienz %", "fr": "Efficacité %"},
    "Completamento %": {"it": "Completamento %", "en": "Completion %", "es": "Completado %", "de": "Fertigstellung %", "fr": "Achèvement %"},
    "TAT medio (gg)": {"it": "TAT medio (gg)", "en": "Avg TAT (days)", "es": "TAT medio (días)", "de": "Durchschn. TAT (Tage)", "fr": "TAT moyen (jours)"},
    "Media (gg)": {"it": "Media (gg)", "en": "Avg (days)", "es": "Media (días)", "de": "Durchschn. (Tage)", "fr": "Moy. (jours)"},
    "Min (gg)": {"it": "Min (gg)", "en": "Min (days)", "es": "Mín (días)", "de": "Min (Tage)", "fr": "Min (jours)"},
    "Max (gg)": {"it": "Max (gg)", "en": "Max (days)", "es": "Máx (días)", "de": "Max (Tage)", "fr": "Max (jours)"},

    # ==========================================================================
    # Common labels
    # ==========================================================================
    "Descrizione:": {"it": "Descrizione:", "en": "Description:", "es": "Descripción:", "de": "Beschreibung:", "fr": "Description :"},
    "Codice:": {"it": "Codice:", "en": "Code:", "es": "Código:", "de": "Code:", "fr": "Code :"},
    "Attivo:": {"it": "Attivo:", "en": "Active:", "es": "Activo:", "de": "Aktiv:", "fr": "Actif :"},
    "Stato": {"it": "Stato", "en": "Status", "es": "Estado", "de": "Status", "fr": "Statut"},
    "Attivi": {"it": "Attivi", "en": "Active", "es": "Activos", "de": "Aktiv", "fr": "Actifs"},
    "Non Attivi": {"it": "Non Attivi", "en": "Inactive", "es": "Inactivos", "de": "Inaktiv", "fr": "Inactifs"},
    "Tutti": {"it": "Tutti", "en": "All", "es": "Todos", "de": "Alle", "fr": "Tous"},
    "Ricerca": {"it": "Ricerca", "en": "Search", "es": "Búsqueda", "de": "Suchen", "fr": "Rechercher"},
    "Totale:": {"it": "Totale:", "en": "Total:", "es": "Total:", "de": "Gesamt:", "fr": "Total :"},
    "Da:": {"it": "Da:", "en": "From:", "es": "Desde:", "de": "Von:", "fr": "De :"},
    "A:": {"it": "A:", "en": "To:", "es": "Hasta:", "de": "Bis:", "fr": "À :"},
    "Periodo rapido:": {"it": "Periodo rapido:", "en": "Quick period:", "es": "Período rápido:", "de": "Schnellauswahl:", "fr": "Période rapide :"},
    "Tipo": {"it": "Tipo", "en": "Type", "es": "Tipo", "de": "Typ", "fr": "Type"},
    "Descrizione": {"it": "Descrizione", "en": "Description", "es": "Descripción", "de": "Beschreibung", "fr": "Description"},
    "Codice": {"it": "Codice", "en": "Code", "es": "Código", "de": "Code", "fr": "Code"},

    # ==========================================================================
    # Warehouse view
    # ==========================================================================
    "Prodotto": {"it": "Prodotto", "en": "Product", "es": "Producto", "de": "Produkt", "fr": "Produit"},
    "Lotto": {"it": "Lotto", "en": "Batch", "es": "Lote", "de": "Charge", "fr": "Lot"},
    "Lotti": {"it": "Lotti", "en": "Batches", "es": "Lotes", "de": "Chargen", "fr": "Lots"},
    "Scadenza": {"it": "Scadenza", "en": "Expiration", "es": "Caducidad", "de": "Ablauf", "fr": "Expiration"},
    "Etichette": {"it": "Etichette", "en": "Labels", "es": "Etiquetas", "de": "Etiketten", "fr": "Étiquettes"},
    "Azione etichetta": {"it": "Azione etichetta", "en": "Label action", "es": "Acción de etiqueta", "de": "Etikett-Aktion", "fr": "Action étiquette"},
    "Evadi": {"it": "Evadi", "en": "Dispatch", "es": "Despachar", "de": "Versenden", "fr": "Expédier"},
    "Prodotti (selezionare categoria)": {"it": "Prodotti (selezionare categoria)", "en": "Products (select category)", "es": "Productos (seleccionar categoría)", "de": "Produkte (Kategorie wählen)", "fr": "Produits (sélectionner catégorie)"},
    "-- Tutte --": {"it": "-- Tutte --", "en": "-- All --", "es": "-- Todas --", "de": "-- Alle --", "fr": "-- Tous --"},
    "Dettagli Prodotto": {"it": "Dettagli Prodotto", "en": "Product Details", "es": "Detalles del Producto", "de": "Produktdetails", "fr": "Détails du produit"},
    "Fornitore:": {"it": "Fornitore:", "en": "Supplier:", "es": "Proveedor:", "de": "Lieferant:", "fr": "Fournisseur :"},
    "Confezionamento:": {"it": "Confezionamento:", "en": "Packaging:", "es": "Envase:", "de": "Verpackung:", "fr": "Conditionnement :"},
    "Conservazione:": {"it": "Conservazione:", "en": "Storage:", "es": "Conservación:", "de": "Lagerung:", "fr": "Stockage :"},
    "Al buio:": {"it": "Al buio:", "en": "In dark:", "es": "En oscuridad:", "de": "Im Dunkeln:", "fr": "Dans l'obscurité :"},
    "Categoria:": {"it": "Categoria:", "en": "Category:", "es": "Categoría:", "de": "Kategorie:", "fr": "Catégorie :"},
    "Giacenza:": {"it": "Giacenza:", "en": "Stock:", "es": "Existencias:", "de": "Bestand:", "fr": "Stock :"},
    "Selezionare un prodotto!": {"it": "Selezionare un prodotto!", "en": "Select a product!", "es": "¡Seleccione un producto!", "de": "Produkt auswählen!", "fr": "Sélectionnez un produit !"},
    "Selezionare un lotto!": {"it": "Selezionare un lotto!", "en": "Select a batch!", "es": "¡Seleccione un lote!", "de": "Charge auswählen!", "fr": "Sélectionnez un lot !"},
    "Scaricare l'etichetta": {"it": "Scaricare l'etichetta", "en": "Unload label", "es": "Descargar etiqueta", "de": "Etikett entladen", "fr": "Décharger l'étiquette"},
    "Ripristinare l'etichetta": {"it": "Ripristinare l'etichetta", "en": "Restore label", "es": "Restaurar etiqueta", "de": "Etikett wiederherstellen", "fr": "Restaurer l'étiquette"},
    "Annullare l'etichetta": {"it": "Annullare l'etichetta", "en": "Cancel label", "es": "Cancelar etiqueta", "de": "Etikett stornieren", "fr": "Annuler l'étiquette"},
    "Etichetta generata e inviata alla stampa.": {"it": "Etichetta generata e inviata alla stampa.", "en": "Label generated and sent to print.", "es": "Etiqueta generada y enviada a imprimir.", "de": "Etikett generiert und zum Drucken gesendet.", "fr": "Étiquette générée et envoyée à l'impression."},
    "Errore nella generazione dell'etichetta:": {"it": "Errore nella generazione dell'etichetta:", "en": "Error generating label:", "es": "Error al generar la etiqueta:", "de": "Fehler bei der Etikettgenerierung:", "fr": "Erreur lors de la génération de l'étiquette :"},

    # ==========================================================================
    # Products view
    # ==========================================================================
    "Nuovo Prodotto": {"it": "Nuovo Prodotto", "en": "New Product", "es": "Nuevo Producto", "de": "Neues Produkt", "fr": "Nouveau produit"},
    "Modifica Prodotto": {"it": "Modifica Prodotto", "en": "Edit Product", "es": "Editar Producto", "de": "Produkt bearbeiten", "fr": "Modifier le produit"},
    "Il campo Codice è obbligatorio!": {"it": "Il campo Codice è obbligatorio!", "en": "Code field is required!", "es": "¡El campo Código es obligatorio!", "de": "Code-Feld ist erforderlich!", "fr": "Le champ Code est requis !"},
    "Il campo Descrizione è obbligatorio!": {"it": "Il campo Descrizione è obbligatorio!", "en": "Description field is required!", "es": "¡El campo Descripción es obligatorio!", "de": "Beschreibung-Feld ist erforderlich!", "fr": "Le champ Description est requis !"},

    # ==========================================================================
    # Packages view
    # ==========================================================================
    "Nuova Confezione": {"it": "Nuova Confezione", "en": "New Package", "es": "Nuevo Envase", "de": "Neue Packung", "fr": "Nouveau conditionnement"},
    "Modifica Confezione": {"it": "Modifica Confezione", "en": "Edit Package", "es": "Editar Envase", "de": "Packung bearbeiten", "fr": "Modifier le conditionnement"},
    "Cod.Forn.": {"it": "Cod.Forn.", "en": "Supp.Code", "es": "Cód.Prov.", "de": "Lief.Code", "fr": "Code fourn."},
    "Fornitore": {"it": "Fornitore", "en": "Supplier", "es": "Proveedor", "de": "Lieferant", "fr": "Fournisseur"},
    "Et.": {"it": "Et.", "en": "Lb.", "es": "Etiq.", "de": "Et.", "fr": "Ét."},
    "Confezionamento": {"it": "Confezionamento", "en": "Packaging", "es": "Envase", "de": "Verpackung", "fr": "Conditionnement"},
    "Conserv.": {"it": "Conserv.", "en": "Storage", "es": "Conserv.", "de": "Lagerung", "fr": "Stockage"},
    "Fonte": {"it": "Fonte", "en": "Source", "es": "Fuente", "de": "Quelle", "fr": "Source"},
    "Cod. Fornitore:": {"it": "Cod. Fornitore:", "en": "Supplier Code:", "es": "Código Proveedor:", "de": "Lieferantencode:", "fr": "Code fournisseur :"},
    "Ubicazione": {"it": "Ubicazione", "en": "Location", "es": "Ubicación", "de": "Standort", "fr": "Emplacement"},
    "Ubicazione:": {"it": "Ubicazione:", "en": "Location:", "es": "Ubicación:", "de": "Standort:", "fr": "Emplacement :"},
    "Fonte:": {"it": "Fonte:", "en": "Source:", "es": "Fuente:", "de": "Quelle:", "fr": "Source :"},
    "Ordinazione:": {"it": "Ordinazione:", "en": "Ordering:", "es": "Pedido:", "de": "Bestellung:", "fr": "Commande :"},
    "Al pezzo": {"it": "Al pezzo", "en": "By piece", "es": "Por unidad", "de": "Pro Stück", "fr": "À la pièce"},
    "A confezione": {"it": "A confezione", "en": "By package", "es": "Por envase", "de": "Pro Packung", "fr": "Par conditionnement"},
    "Pezzi per etichetta:": {"it": "Pezzi per etichetta:", "en": "Pieces per label:", "es": "Piezas por etiqueta:", "de": "Stück pro Etikett:", "fr": "Pièces par étiquette :"},
    "Soglia riordino:": {"it": "Soglia riordino:", "en": "Reorder level:", "es": "Nivel de reorden:", "de": "Nachbestellgrenze:", "fr": "Seuil de réapprovisionnement :"},
    "-- Non assegnata --": {"it": "-- Non assegnata --", "en": "-- Not assigned --", "es": "-- Sin asignar --", "de": "-- Nicht zugewiesen --", "fr": "-- Non assigné --"},
    "Selezionare un fornitore!": {"it": "Selezionare un fornitore!", "en": "Select a supplier!", "es": "¡Seleccione un proveedor!", "de": "Lieferant auswählen!", "fr": "Sélectionnez un fournisseur !"},
    "Il campo Codice Fornitore è obbligatorio!": {"it": "Il campo Codice Fornitore è obbligatorio!", "en": "Supplier Code field is required!", "es": "¡El campo Código Proveedor es obligatorio!", "de": "Lieferantencode-Feld ist erforderlich!", "fr": "Le champ Code fournisseur est requis !"},
    "Il campo Confezionamento è obbligatorio!": {"it": "Il campo Confezionamento è obbligatorio!", "en": "Packaging field is required!", "es": "¡El campo Envase es obligatorio!", "de": "Verpackung-Feld ist erforderlich!", "fr": "Le champ Conditionnement est requis !"},
    "Selezionare una modalità di conservazione!": {"it": "Selezionare una modalità di conservazione!", "en": "Select a storage condition!", "es": "¡Seleccione una condición de almacenamiento!", "de": "Lagerbedingung auswählen!", "fr": "Sélectionnez une condition de stockage !"},

    # ==========================================================================
    # Suppliers view
    # ==========================================================================
    "Nuovo Fornitore": {"it": "Nuovo Fornitore", "en": "New Supplier", "es": "Nuevo Proveedor", "de": "Neuer Lieferant", "fr": "Nouveau fournisseur"},
    "Modifica Fornitore": {"it": "Modifica Fornitore", "en": "Edit Supplier", "es": "Editar Proveedor", "de": "Lieferant bearbeiten", "fr": "Modifier le fournisseur"},

    # ==========================================================================
    # Categories view
    # ==========================================================================
    "Nuova Categoria": {"it": "Nuova Categoria", "en": "New Category", "es": "Nueva Categoría", "de": "Neue Kategorie", "fr": "Nouvelle catégorie"},
    "Modifica Categoria": {"it": "Modifica Categoria", "en": "Edit Category", "es": "Editar Categoría", "de": "Kategorie bearbeiten", "fr": "Modifier la catégorie"},

    # ==========================================================================
    # Locations view
    # ==========================================================================
    "Nuova Ubicazione": {"it": "Nuova Ubicazione", "en": "New Location", "es": "Nueva Ubicación", "de": "Neuer Standort", "fr": "Nouvel emplacement"},
    "Modifica Ubicazione": {"it": "Modifica Ubicazione", "en": "Edit Location", "es": "Editar Ubicación", "de": "Standort bearbeiten", "fr": "Modifier l'emplacement"},
    "Stanza:": {"it": "Stanza:", "en": "Room:", "es": "Sala:", "de": "Raum:", "fr": "Salle :"},

    # ==========================================================================
    # Conservations view
    # ==========================================================================
    "Nuova Conservazione": {"it": "Nuova Conservazione", "en": "New Storage Condition", "es": "Nueva Condición de Almacenamiento", "de": "Neue Lagerbedingung", "fr": "Nouvelle condition de stockage"},
    "Modifica Conservazione": {"it": "Modifica Conservazione", "en": "Edit Storage Condition", "es": "Editar Condición de Almacenamiento", "de": "Lagerbedingung bearbeiten", "fr": "Modifier la condition de stockage"},

    # ==========================================================================
    # Funding sources view
    # ==========================================================================
    "Nuova Fonte": {"it": "Nuova Fonte", "en": "New Funding Source", "es": "Nueva Fuente de Financiación", "de": "Neue Finanzierungsquelle", "fr": "Nouvelle source de financement"},
    "Modifica Fonte": {"it": "Modifica Fonte", "en": "Edit Funding Source", "es": "Editar Fuente de Financiación", "de": "Finanzierungsquelle bearbeiten", "fr": "Modifier la source de financement"},

    # ==========================================================================
    # Batch view
    # ==========================================================================
    "Modifica Lotto": {"it": "Modifica Lotto", "en": "Edit Batch", "es": "Editar Lote", "de": "Charge bearbeiten", "fr": "Modifier le lot"},
    "Lotto:": {"it": "Lotto:", "en": "Batch:", "es": "Lote:", "de": "Charge:", "fr": "Lot :"},
    "Scadenza:": {"it": "Scadenza:", "en": "Expiration:", "es": "Caducidad:", "de": "Ablauf:", "fr": "Expiration :"},
    "Il campo Lotto è obbligatorio!": {"it": "Il campo Lotto è obbligatorio!", "en": "Batch field is required!", "es": "¡El campo Lote es obligatorio!", "de": "Charge-Feld ist erforderlich!", "fr": "Le champ Lot est requis !"},
    "Il campo Scadenza è obbligatorio!": {"it": "Il campo Scadenza è obbligatorio!", "en": "Expiration field is required!", "es": "¡El campo Caducidad es obligatorio!", "de": "Ablauf-Feld ist erforderlich!", "fr": "Le champ Expiration est requis !"},

    # ==========================================================================
    # Labels view
    # ==========================================================================
    "Carica etichette": {"it": "Carica etichette", "en": "Load labels", "es": "Cargar etiquetas", "de": "Etiketten laden", "fr": "Charger les étiquettes"},
    "Quantità:": {"it": "Quantità:", "en": "Quantity:", "es": "Cantidad:", "de": "Menge:", "fr": "Quantité :"},
    "Numero etichette da creare:": {"it": "Numero etichette da creare:", "en": "Number of labels to create:", "es": "Número de etiquetas a crear:", "de": "Anzahl zu erstellender Etiketten:", "fr": "Nombre d'étiquettes à créer :"},
    "Etichette create:": {"it": "Etichette create:", "en": "Labels created:", "es": "Etiquetas creadas:", "de": "Etiketten erstellt:", "fr": "Étiquettes créées :"},

    # ==========================================================================
    # Requests view
    # ==========================================================================
    "Riferimento": {"it": "Riferimento", "en": "Reference", "es": "Referencia", "de": "Referenz", "fr": "Référence"},
    "Data": {"it": "Data", "en": "Date", "es": "Fecha", "de": "Datum", "fr": "Date"},
    "Dettaglio Richiesta": {"it": "Dettaglio Richiesta", "en": "Request Details", "es": "Detalles de Solicitud", "de": "Anfragedetails", "fr": "Détails de la demande"},
    "Aggiungi Articolo": {"it": "Aggiungi Articolo", "en": "Add Item", "es": "Agregar Artículo", "de": "Artikel hinzufügen", "fr": "Ajouter un article"},
    "Modifica Articolo": {"it": "Modifica Articolo", "en": "Edit Item", "es": "Editar Artículo", "de": "Artikel bearbeiten", "fr": "Modifier l'article"},
    "Elimina Articolo": {"it": "Elimina Articolo", "en": "Delete Item", "es": "Eliminar Artículo", "de": "Artikel löschen", "fr": "Supprimer l'article"},
    "Chiudi Richiesta": {"it": "Chiudi Richiesta", "en": "Close Request", "es": "Cerrar Solicitud", "de": "Anfrage schließen", "fr": "Fermer la demande"},
    "Elimina Richiesta": {"it": "Elimina Richiesta", "en": "Delete Request", "es": "Eliminar Solicitud", "de": "Anfrage löschen", "fr": "Supprimer la demande"},
    "Aperte": {"it": "Aperte", "en": "Open", "es": "Abiertas", "de": "Offen", "fr": "Ouvertes"},
    "Chiuse": {"it": "Chiuse", "en": "Closed", "es": "Cerradas", "de": "Geschlossen", "fr": "Fermées"},
    "Tutte": {"it": "Tutte", "en": "All", "es": "Todas", "de": "Alle", "fr": "Tous"},
    "Generare una nuova richiesta?": {"it": "Generare una nuova richiesta?", "en": "Generate a new request?", "es": "¿Generar una nueva solicitud?", "de": "Neue Anfrage erstellen?", "fr": "Générer une nouvelle demande ?"},
    "Nuova Richiesta": {"it": "Nuova Richiesta", "en": "New Request", "es": "Nueva Solicitud", "de": "Neue Anfrage", "fr": "Nouvelle demande"},
    "Modifica Richiesta": {"it": "Modifica Richiesta", "en": "Edit Request", "es": "Editar Solicitud", "de": "Anfrage bearbeiten", "fr": "Modifier la demande"},
    "Riferimento:": {"it": "Riferimento:", "en": "Reference:", "es": "Referencia:", "de": "Referenz:", "fr": "Référence :"},
    "Data:": {"it": "Data:", "en": "Date:", "es": "Fecha:", "de": "Datum:", "fr": "Date :"},
    "Articoli": {"it": "Articoli", "en": "Items", "es": "Artículos", "de": "Artikel", "fr": "Articles"},
    "Rimuovi Articolo": {"it": "Rimuovi Articolo", "en": "Remove Item", "es": "Quitar Artículo", "de": "Artikel entfernen", "fr": "Retirer l'article"},
    "Quantità": {"it": "Quantità", "en": "Quantity", "es": "Cantidad", "de": "Menge", "fr": "Quantité"},
    "Consegnato": {"it": "Consegnato", "en": "Delivered", "es": "Entregado", "de": "Geliefert", "fr": "Livré"},
    "Confezione:": {"it": "Confezione:", "en": "Package:", "es": "Envase:", "de": "Packung:", "fr": "Conditionnement :"},
    "Nuovo Articolo": {"it": "Nuovo Articolo", "en": "New Item", "es": "Nuevo Artículo", "de": "Neuer Artikel", "fr": "Nouvel article"},
    "Ord": {"it": "Ord", "en": "Ord", "es": "Ped", "de": "Best.", "fr": "Com."},
    "Eva": {"it": "Eva", "en": "Del", "es": "Ent", "de": "Lief.", "fr": "Livré"},
    "Selezionare una categoria!": {"it": "Selezionare una categoria!", "en": "Select a category!", "es": "¡Seleccione una categoría!", "de": "Kategorie auswählen!", "fr": "Sélectionnez une catégorie !"},
    "Selezionare una confezione!": {"it": "Selezionare una confezione!", "en": "Select a package!", "es": "¡Seleccione un envase!", "de": "Packung auswählen!", "fr": "Sélectionnez un conditionnement !"},
    "La quantità deve essere almeno 1!": {"it": "La quantità deve essere almeno 1!", "en": "Quantity must be at least 1!", "es": "¡La cantidad debe ser al menos 1!", "de": "Menge muss mindestens 1 sein!", "fr": "La quantité doit être au moins 1 !"},
    "Articolo già presente.": {"it": "Articolo già presente.", "en": "Item already exists.", "es": "Artículo ya existe.", "de": "Artikel existiert bereits.", "fr": "L'article existe déjà."},
    "La quantità è stata sommata.": {"it": "La quantità è stata sommata.", "en": "Quantity has been added.", "es": "La cantidad ha sido sumada.", "de": "Menge wurde hinzugefügt.", "fr": "La quantité a été ajoutée."},
    "Bozze": {"it": "Bozze", "en": "Drafts", "es": "Borradores", "de": "Entwürfe", "fr": "Brouillons"},
    "Inviate": {"it": "Inviate", "en": "Sent", "es": "Enviadas", "de": "Gesendet", "fr": "Envoyées"},
    "Invia Richiesta": {"it": "Invia Richiesta", "en": "Send Request", "es": "Enviar Solicitud", "de": "Anfrage senden", "fr": "Envoyer la demande"},
    "Solo le bozze possono essere modificate!": {"it": "Solo le bozze possono essere modificate!", "en": "Only drafts can be edited!", "es": "¡Solo los borradores pueden ser editados!", "de": "Nur Entwürfe können bearbeitet werden!", "fr": "Seuls les brouillons peuvent être modifiés !"},
    "Solo le bozze possono essere inviate!": {"it": "Solo le bozze possono essere inviate!", "en": "Only drafts can be sent!", "es": "¡Solo los borradores pueden ser enviados!", "de": "Nur Entwürfe können gesendet werden!", "fr": "Seuls les brouillons peuvent être envoyés !"},
    "Impossibile inviare una richiesta senza articoli!": {"it": "Impossibile inviare una richiesta senza articoli!", "en": "Cannot send a request without items!", "es": "¡No se puede enviar una solicitud sin artículos!", "de": "Anfrage ohne Artikel kann nicht gesendet werden!", "fr": "Impossible d'envoyer une demande sans articles !"},
    "Inviare la richiesta selezionata?": {"it": "Inviare la richiesta selezionata?", "en": "Send the selected request?", "es": "¿Enviar la solicitud seleccionada?", "de": "Ausgewählte Anfrage senden?", "fr": "Envoyer la demande sélectionnée ?"},
    "Articoli modificabili solo nelle bozze!": {"it": "Articoli modificabili solo nelle bozze!", "en": "Items can only be edited in drafts!", "es": "¡Los artículos solo pueden editarse en borradores!", "de": "Artikel können nur in Entwürfen bearbeitet werden!", "fr": "Les articles ne peuvent être modifiés que dans les brouillons !"},
    "Articoli eliminabili solo nelle bozze!": {"it": "Articoli eliminabili solo nelle bozze!", "en": "Items can only be deleted in drafts!", "es": "¡Los artículos solo pueden eliminarse en borradores!", "de": "Artikel können nur in Entwürfen gelöscht werden!", "fr": "Les articles ne peuvent être supprimés que dans les brouillons !"},
    "Articoli annullabili solo nelle richieste inviate!": {"it": "Articoli annullabili solo nelle richieste inviate!", "en": "Items can only be cancelled in sent requests!", "es": "¡Los artículos solo pueden anularse en solicitudes enviadas!", "de": "Artikel können nur in gesendeten Anfragen storniert werden!", "fr": "Les articles ne peuvent être annulés que dans les demandes envoyées !"},
    "Le bozze non possono essere chiuse.": {"it": "Le bozze non possono essere chiuse.", "en": "Drafts cannot be closed.", "es": "Los borradores no pueden cerrarse.", "de": "Entwürfe können nicht geschlossen werden.", "fr": "Les brouillons ne peuvent pas être fermés."},
    "Inviarle prima o eliminarle.": {"it": "Inviarle prima o eliminarle.", "en": "Send them first or delete them.", "es": "Envíelos primero o elimínelos.", "de": "Erst senden oder löschen.", "fr": "Envoyez-les d'abord ou supprimez-les."},
    "La richiesta è già chiusa!": {"it": "La richiesta è già chiusa!", "en": "The request is already closed!", "es": "¡La solicitud ya está cerrada!", "de": "Die Anfrage ist bereits geschlossen!", "fr": "La demande est déjà fermée !"},
    "Chiudere la richiesta selezionata?": {"it": "Chiudere la richiesta selezionata?", "en": "Close the selected request?", "es": "¿Cerrar la solicitud seleccionada?", "de": "Ausgewählte Anfrage schließen?", "fr": "Fermer la demande sélectionnée ?"},
    "Annullato": {"it": "Annullato", "en": "Cancelled", "es": "Anulado", "de": "Storniert", "fr": "Annulé"},
    "Nota": {"it": "Nota", "en": "Note", "es": "Nota", "de": "Notiz", "fr": "Note"},
    "Non ci sono più articoli attivi.": {"it": "Non ci sono più articoli attivi.", "en": "There are no more active items.", "es": "No hay más artículos activos.", "de": "Keine aktiven Artikel mehr.", "fr": "Il n'y a plus d'articles actifs."},
    "Chiudere la richiesta?": {"it": "Chiudere la richiesta?", "en": "Close the request?", "es": "¿Cerrar la solicitud?", "de": "Anfrage schließen?", "fr": "Fermer la demande ?"},
    "Motivo annullamento:": {"it": "Motivo annullamento:", "en": "Cancellation reason:", "es": "Motivo de anulación:", "de": "Stornierungsgrund:", "fr": "Motif d'annulation :"},
    "Annulla Articolo": {"it": "Annulla Articolo", "en": "Cancel Item", "es": "Anular Artículo", "de": "Artikel stornieren", "fr": "Annuler l'article"},
    "Inserire il motivo dell'annullamento!": {"it": "Inserire il motivo dell'annullamento!", "en": "Enter the cancellation reason!", "es": "¡Ingrese el motivo de la anulación!", "de": "Stornierungsgrund eingeben!", "fr": "Entrez le motif d'annulation !"},
    "Confermare l'annullamento dell'articolo?": {"it": "Confermare l'annullamento dell'articolo?", "en": "Confirm item cancellation?", "es": "¿Confirmar anulación del artículo?", "de": "Artikelstornierung bestätigen?", "fr": "Confirmer l'annulation de l'article ?"},
    "L'articolo è già stato annullato.": {"it": "L'articolo è già stato annullato.", "en": "The item has already been cancelled.", "es": "El artículo ya ha sido anulado.", "de": "Der Artikel wurde bereits storniert.", "fr": "L'article a déjà été annulé."},
    "Impossibile eliminare un articolo annullato.": {"it": "Impossibile eliminare un articolo annullato.", "en": "Cannot delete a cancelled item.", "es": "No se puede eliminar un artículo anulado.", "de": "Stornierter Artikel kann nicht gelöscht werden.", "fr": "Impossible de supprimer un article annulé."},
    "Articolo annullato.": {"it": "Articolo annullato.", "en": "Item cancelled.", "es": "Artículo anulado.", "de": "Artikel storniert.", "fr": "Article annulé."},
    "Motivo": {"it": "Motivo", "en": "Reason", "es": "Motivo", "de": "Grund", "fr": "Motif"},
    "Dettaglio:": {"it": "Dettaglio:", "en": "Detail:", "es": "Detalle:", "de": "Detail:", "fr": "Détail :"},
    "Nota:": {"it": "Nota:", "en": "Note:", "es": "Nota:", "de": "Notiz:", "fr": "Note :"},
    "Eliminare l'articolo selezionato?": {"it": "Eliminare l'articolo selezionato?", "en": "Delete the selected item?", "es": "¿Eliminar el artículo seleccionado?", "de": "Ausgewählten Artikel löschen?", "fr": "Supprimer l'article sélectionné ?"},
    "Eliminare la richiesta '{}' e tutti i suoi articoli?": {"it": "Eliminare la richiesta '{}' e tutti i suoi articoli?", "en": "Delete request '{}' and all its items?", "es": "¿Eliminar la solicitud '{}' y todos sus artículos?", "de": "Anfrage '{}' und alle Artikel löschen?", "fr": "Supprimer la demande '{}' et tous ses articles ?"},
    "La richiesta non contiene articoli.": {"it": "La richiesta non contiene articoli.", "en": "The request contains no items.", "es": "La solicitud no contiene artículos.", "de": "Die Anfrage enthält keine Artikel.", "fr": "La demande ne contient aucun article."},
    "Errore nella generazione del report:": {"it": "Errore nella generazione del report:", "en": "Error generating report:", "es": "Error al generar el informe:", "de": "Fehler bei der Berichtserstellung:", "fr": "Erreur lors de la génération du rapport :"},
    "Selezionare prima una richiesta!": {"it": "Selezionare prima una richiesta!", "en": "Select a request first!", "es": "¡Seleccione primero una solicitud!", "de": "Zuerst eine Anfrage auswählen!", "fr": "Sélectionnez d'abord une demande !"},
    "Selezionare un articolo!": {"it": "Selezionare un articolo!", "en": "Select an item!", "es": "¡Seleccione un artículo!", "de": "Artikel auswählen!", "fr": "Sélectionnez un élément !"},
    "Stampa disabilitata su questa postazione.": {"it": "Stampa disabilitata su questa postazione.", "en": "Printing disabled on this workstation.", "es": "Impresión deshabilitada en esta estación.", "de": "Drucken auf dieser Arbeitsstation deaktiviert.", "fr": "Impression désactivée sur ce poste."},
    "Impostazioni locali": {"it": "Impostazioni locali", "en": "Local settings", "es": "Configuración local", "de": "Lokale Einstellungen", "fr": "Paramètres locaux"},
    "Stampa etichette:": {"it": "Stampa etichette:", "en": "Label printing:", "es": "Impresión de etiquetas:", "de": "Etikettendruck:", "fr": "Impression d'étiquettes :"},
    "Abilitata su questa postazione": {"it": "Abilitata su questa postazione", "en": "Enabled on this workstation", "es": "Habilitada en esta estación", "de": "Auf dieser Arbeitsstation aktiviert", "fr": "Activée sur ce poste"},

    # ==========================================================================
    # Delivery view
    # ==========================================================================
    "Nuova Consegna": {"it": "Nuova Consegna", "en": "New Delivery", "es": "Nueva Entrega", "de": "Neue Lieferung", "fr": "Nouvelle livraison"},
    "Registra Consegna": {"it": "Registra Consegna", "en": "Record Delivery", "es": "Registrar Entrega", "de": "Lieferung erfassen", "fr": "Enregistrer la livraison"},
    "Data consegna:": {"it": "Data consegna:", "en": "Delivery date:", "es": "Fecha de entrega:", "de": "Lieferdatum:", "fr": "Date de livraison :"},
    "Quantità consegnata:": {"it": "Quantità consegnata:", "en": "Quantity delivered:", "es": "Cantidad entregada:", "de": "Gelieferte Menge:", "fr": "Quantité livrée :"},
    "Richieste aperte": {"it": "Richieste aperte", "en": "Open requests", "es": "Solicitudes abiertas", "de": "Offene Anfragen", "fr": "Demandes ouvertes"},
    "Richieste Aperte": {"it": "Richieste Aperte", "en": "Open Requests", "es": "Solicitudes Abiertas", "de": "Offene Anfragen", "fr": "Demandes ouvertes"},
    "Seleziona richiesta": {"it": "Seleziona richiesta", "en": "Select request", "es": "Seleccionar solicitud", "de": "Anfrage auswählen", "fr": "Sélectionner la demande"},
    "Articoli da Evadere": {"it": "Articoli da Evadere", "en": "Items to Fulfill", "es": "Artículos a Despachar", "de": "Zu erfüllende Artikel", "fr": "Articles à traiter"},
    "Dettaglio Articolo": {"it": "Dettaglio Articolo", "en": "Item Details", "es": "Detalle del Artículo", "de": "Artikeldetails", "fr": "Détails de l'article"},
    "Già Evaso:": {"it": "Già Evaso:", "en": "Already Fulfilled:", "es": "Ya Despachado:", "de": "Bereits erfüllt:", "fr": "Déjà traité :"},
    "DDT:": {"it": "DDT:", "en": "Delivery Note:", "es": "Albarán:", "de": "Lieferschein:", "fr": "Bon de livraison :"},
    "Data Consegna:": {"it": "Data Consegna:", "en": "Delivery Date:", "es": "Fecha de Entrega:", "de": "Lieferdatum:", "fr": "Date de livraison :"},
    "Seleziona esistente:": {"it": "Seleziona esistente:", "en": "Select existing:", "es": "Seleccionar existente:", "de": "Vorhandene auswählen:", "fr": "Sélectionner existant :"},
    "Crea nuovo:": {"it": "Crea nuovo:", "en": "Create new:", "es": "Crear nuevo:", "de": "Neu erstellen:", "fr": "Créer nouveau :"},
    "Scad": {"it": "Scad", "en": "Exp", "es": "Cad", "de": "Abl.", "fr": "Exp"},
    "Selezionare un articolo da evadere!": {"it": "Selezionare un articolo da evadere!", "en": "Select an item to fulfill!", "es": "¡Seleccione un artículo a despachar!", "de": "Artikel zur Erfüllung auswählen!", "fr": "Sélectionnez un article à traiter !"},
    "Inserire il numero DDT!": {"it": "Inserire il numero DDT!", "en": "Enter the delivery note number!", "es": "¡Ingrese el número del albarán!", "de": "Lieferscheinnummer eingeben!", "fr": "Entrez le numéro du bon de livraison !"},
    "Data consegna non valida!": {"it": "Data consegna non valida!", "en": "Invalid delivery date!", "es": "¡Fecha de entrega no válida!", "de": "Ungültiges Lieferdatum!", "fr": "Date de livraison invalide !"},
    "La quantità deve essere tra 1 e": {"it": "La quantità deve essere tra 1 e", "en": "Quantity must be between 1 and", "es": "La cantidad debe estar entre 1 y", "de": "Menge muss zwischen 1 und", "fr": "La quantité doit être entre 1 et"},
    "La quantità deve essere un multiplo di": {"it": "La quantità deve essere un multiplo di", "en": "Quantity must be a multiple of", "es": "La cantidad debe ser múltiplo de", "de": "Menge muss ein Vielfaches von", "fr": "La quantité doit être un multiple de"},
    "Selezionare un lotto esistente!": {"it": "Selezionare un lotto esistente!", "en": "Select an existing batch!", "es": "¡Seleccione un lote existente!", "de": "Vorhandene Charge auswählen!", "fr": "Sélectionnez un lot existant !"},
    "Inserire il numero di lotto!": {"it": "Inserire il numero di lotto!", "en": "Enter the batch number!", "es": "¡Ingrese el número de lote!", "de": "Chargennummer eingeben!", "fr": "Entrez le numéro de lot !"},
    "Data scadenza non valida!": {"it": "Data scadenza non valida!", "en": "Invalid expiration date!", "es": "¡Fecha de caducidad no válida!", "de": "Ungültiges Ablaufdatum!", "fr": "Date d'expiration invalide !"},
    "La data di scadenza deve essere futura!": {"it": "La data di scadenza deve essere futura!", "en": "Expiration date must be in the future!", "es": "¡La fecha de caducidad debe ser futura!", "de": "Ablaufdatum muss in der Zukunft liegen!", "fr": "La date d'expiration doit être dans le futur !"},
    "Il lotto": {"it": "Il lotto", "en": "Batch", "es": "El lote", "de": "Charge", "fr": "Lot"},
    "con scadenza": {"it": "con scadenza", "en": "with expiration", "es": "con caducidad", "de": "mit Ablauf", "fr": "avec expiration"},
    "Selezionarlo dalla lista dei lotti esistenti.": {"it": "Selezionarlo dalla lista dei lotti esistenti.", "en": "Select it from the existing batches list.", "es": "Selecciónelo de la lista de lotes existentes.", "de": "Aus der Liste der vorhandenen Chargen auswählen.", "fr": "Sélectionnez-le dans la liste des lots existants."},
    "Registrare la consegna di": {"it": "Registrare la consegna di", "en": "Record delivery of", "es": "Registrar entrega de", "de": "Lieferung erfassen von", "fr": "Enregistrer la livraison de"},
    "unità?": {"it": "unità?", "en": "units?", "es": "unidades?", "de": "Einheiten?", "fr": "unités ?"},
    "Verranno create": {"it": "Verranno create", "en": "Will create", "es": "Se crearán", "de": "Wird erstellen", "fr": "Va créer"},
    "etichette.": {"it": "etichette.", "en": "labels.", "es": "etiquetas.", "de": "Etiketten.", "fr": "étiquettes."},
    "etichetta": {"it": "etichetta", "en": "label", "es": "etiqueta", "de": "Etikett", "fr": "étiquette"},
    "Errore nella creazione del lotto!": {"it": "Errore nella creazione del lotto!", "en": "Error creating batch!", "es": "¡Error al crear el lote!", "de": "Fehler beim Erstellen der Charge!", "fr": "Erreur lors de la création du lot !"},
    "Errore nella registrazione della consegna!": {"it": "Errore nella registrazione della consegna!", "en": "Error recording delivery!", "es": "¡Error al registrar la entrega!", "de": "Fehler beim Erfassen der Lieferung!", "fr": "Erreur lors de l'enregistrement de la livraison !"},
    "Consegna registrata con successo!": {"it": "Consegna registrata con successo!", "en": "Delivery recorded successfully!", "es": "¡Entrega registrada con éxito!", "de": "Lieferung erfolgreich erfasst!", "fr": "Livraison enregistrée avec succès !"},
    "Create": {"it": "Create", "en": "Created", "es": "Creadas", "de": "Erstellt", "fr": "Créées"},
    "Errore durante il salvataggio:": {"it": "Errore durante il salvataggio:", "en": "Error during save:", "es": "Error al guardar:", "de": "Fehler beim Speichern:", "fr": "Erreur lors de l'enregistrement :"},
    "Tutti gli articoli sono stati evasi.": {"it": "Tutti gli articoli sono stati evasi.", "en": "All items have been fulfilled.", "es": "Todos los artículos han sido despachados.", "de": "Alle Artikel wurden erfüllt.", "fr": "Tous les articles ont été traités."},
    "La richiesta è stata chiusa.": {"it": "La richiesta è stata chiusa.", "en": "The request has been closed.", "es": "La solicitud ha sido cerrada.", "de": "Die Anfrage wurde geschlossen.", "fr": "La demande a été fermée."},

    # ==========================================================================
    # Stocks view
    # ==========================================================================
    "Tipo Stampa": {"it": "Tipo Stampa", "en": "Print Type", "es": "Tipo de Impresión", "de": "Drucktyp", "fr": "Type d'impression"},
    "Stampa giacenze": {"it": "Stampa giacenze", "en": "Print stock", "es": "Imprimir existencias", "de": "Bestand drucken", "fr": "Imprimer le stock"},
    "Esporta": {"it": "Esporta", "en": "Export", "es": "Exportar", "de": "Exportieren", "fr": "Exporter"},

    # ==========================================================================
    # Expiring view
    # ==========================================================================
    "Lotti Scaduti": {"it": "Lotti Scaduti", "en": "Expired Batches", "es": "Lotes Caducados", "de": "Abgelaufene Chargen", "fr": "Lots expirés"},
    "Scadenze prossime": {"it": "Scadenze prossime", "en": "Upcoming expirations", "es": "Próximas caducidades", "de": "Bevorstehende Abläufe", "fr": "Expirations à venir"},
    "Giorni:": {"it": "Giorni:", "en": "Days:", "es": "Días:", "de": "Tage:", "fr": "Jours :"},
    "Giorni alla scadenza": {"it": "Giorni alla scadenza", "en": "Days to expiration", "es": "Días hasta caducidad", "de": "Tage bis Ablauf", "fr": "Jours avant expiration"},

    # ==========================================================================
    # Barcode view
    # ==========================================================================
    "Scarico etichette": {"it": "Scarico etichette", "en": "Unload labels", "es": "Descarga de etiquetas", "de": "Etiketten entladen", "fr": "Décharger les étiquettes"},
    "Scarico Etichetta": {"it": "Scarico Etichetta", "en": "Unload Label", "es": "Descargar Etiqueta", "de": "Etikett entladen", "fr": "Décharger l'étiquette"},
    "Scansiona il barcode o inserisci il codice etichetta:": {"it": "Scansiona il barcode o inserisci il codice etichetta:", "en": "Scan barcode or enter label code:", "es": "Escanear código de barras o ingresar código de etiqueta:", "de": "Barcode scannen oder Etikettencode eingeben:", "fr": "Scanner le code-barres ou entrer le code étiquette :"},
    "Codice a barre:": {"it": "Codice a barre:", "en": "Barcode:", "es": "Código de barras:", "de": "Barcode:", "fr": "Code-barres :"},
    "Codice non valido!": {"it": "Codice non valido!", "en": "Invalid code!", "es": "¡Código inválido!", "de": "Ungültiger Code!", "fr": "Code invalide !"},
    "Etichetta": {"it": "Etichetta", "en": "Label", "es": "Etiqueta", "de": "Etikett", "fr": "Étiquette"},
    "non trovata!": {"it": "non trovata!", "en": "not found!", "es": "¡no encontrada!", "de": "nicht gefunden!", "fr": "non trouvée !"},
    "già scaricata!": {"it": "già scaricata!", "en": "already unloaded!", "es": "¡ya descargada!", "de": "bereits entladen!", "fr": "déjà déchargée !"},
    "annullata!": {"it": "annullata!", "en": "cancelled!", "es": "¡cancelada!", "de": "storniert!", "fr": "annulée !"},
    "Scaricata:": {"it": "Scaricata:", "en": "Unloaded:", "es": "Descargada:", "de": "Entladen:", "fr": "Déchargée :"},
    "Errore nello scarico!": {"it": "Errore nello scarico!", "en": "Error unloading!", "es": "¡Error al descargar!", "de": "Fehler beim Entladen!", "fr": "Erreur lors du déchargement !"},
    "Etichetta scaricata:": {"it": "Etichetta scaricata:", "en": "Label unloaded:", "es": "Etiqueta descargada:", "de": "Etikett entladen:", "fr": "Étiquette déchargée :"},
    "Etichetta non trovata!": {"it": "Etichetta non trovata!", "en": "Label not found!", "es": "¡Etiqueta no encontrada!", "de": "Etikett nicht gefunden!", "fr": "Étiquette non trouvée !"},
    "Etichetta già scaricata!": {"it": "Etichetta già scaricata!", "en": "Label already unloaded!", "es": "¡Etiqueta ya descargada!", "de": "Etikett bereits entladen!", "fr": "Étiquette déjà déchargée !"},

    # ==========================================================================
    # Custom label view
    # ==========================================================================
    "Righe da stampare": {"it": "Righe da stampare", "en": "Lines to print", "es": "Líneas a imprimir", "de": "Zu druckende Zeilen", "fr": "Lignes à imprimer"},
    "Testo Etichetta": {"it": "Testo Etichetta", "en": "Label Text", "es": "Texto de Etiqueta", "de": "Etikettentext", "fr": "Texte de l'étiquette"},
    "Includi nome laboratorio": {"it": "Includi nome laboratorio", "en": "Include laboratory name", "es": "Incluir nombre del laboratorio", "de": "Laborname einschließen", "fr": "Inclure le nom du laboratoire"},
    "Modelli Salvati": {"it": "Modelli Salvati", "en": "Saved Templates", "es": "Plantillas Guardadas", "de": "Gespeicherte Vorlagen", "fr": "Modèles enregistrés"},
    "Etichetta personalizzata": {"it": "Etichetta personalizzata", "en": "Custom label", "es": "Etiqueta personalizada", "de": "Benutzerdefiniertes Etikett", "fr": "Étiquette personnalisée"},
    "Testo riga 1:": {"it": "Testo riga 1:", "en": "Text line 1:", "es": "Texto línea 1:", "de": "Textzeile 1:", "fr": "Ligne de texte 1 :"},
    "Testo riga 2:": {"it": "Testo riga 2:", "en": "Text line 2:", "es": "Texto línea 2:", "de": "Textzeile 2:", "fr": "Ligne de texte 2 :"},
    "Testo riga 3:": {"it": "Testo riga 3:", "en": "Text line 3:", "es": "Texto línea 3:", "de": "Textzeile 3:", "fr": "Ligne de texte 3 :"},
    "Codice barcode:": {"it": "Codice barcode:", "en": "Barcode code:", "es": "Código de barras:", "de": "Barcode-Code:", "fr": "Code code-barres :"},

    # ==========================================================================
    # Statistics views
    # ==========================================================================
    "Periodo di Analisi": {"it": "Periodo di Analisi", "en": "Analysis Period", "es": "Período de Análisis", "de": "Analysezeitraum", "fr": "Période d'analyse"},
    "Riepilogo": {"it": "Riepilogo", "en": "Summary", "es": "Resumen", "de": "Zusammenfassung", "fr": "Résumé"},
    "Analisi Scadenze": {"it": "Analisi Scadenze", "en": "Expiration Analysis", "es": "Análisis de Caducidades", "de": "Ablaufanalyse", "fr": "Analyse des expirations"},
    "Analisi Storica Scaduti": {"it": "Analisi Storica Scaduti", "en": "Historical Expired Analysis", "es": "Análisis Histórico de Caducados", "de": "Historische Ablaufanalyse", "fr": "Analyse historique des expirations"},
    "Periodo scadenza - Da:": {"it": "Periodo scadenza - Da:", "en": "Expiration period - From:", "es": "Período de caducidad - Desde:", "de": "Ablaufzeitraum - Von:", "fr": "Période d'expiration - De :"},
    "Anno scorso": {"it": "Anno scorso", "en": "Last year", "es": "Año pasado", "de": "Letztes Jahr", "fr": "Année dernière"},
    "6 mesi fa": {"it": "6 mesi fa", "en": "6 months ago", "es": "Hace 6 meses", "de": "Vor 6 Monaten", "fr": "Il y a 6 mois"},
    "Oggi": {"it": "Oggi", "en": "Today", "es": "Hoy", "de": "Heute", "fr": "Aujourd'hui"},
    "+30 gg": {"it": "+30 gg", "en": "+30 days", "es": "+30 días", "de": "+30 Tage", "fr": "+30 jours"},
    "+90 gg": {"it": "+90 gg", "en": "+90 days", "es": "+90 días", "de": "+90 Tage", "fr": "+90 jours"},
    "30 gg": {"it": "30 gg", "en": "30 days", "es": "30 días", "de": "30 Tage", "fr": "30 jours"},
    "90 gg": {"it": "90 gg", "en": "90 days", "es": "90 días", "de": "90 Tage", "fr": "90 jours"},
    "6 mesi": {"it": "6 mesi", "en": "6 months", "es": "6 meses", "de": "6 Monate", "fr": "6 mois"},
    "Anno": {"it": "Anno", "en": "Year", "es": "Año", "de": "Jahr", "fr": "Année"},
    "Lotti Scaduti (con giacenza residua)": {"it": "Lotti Scaduti (con giacenza residua)", "en": "Expired Batches (with remaining stock)", "es": "Lotes Caducados (con existencias restantes)", "de": "Abgelaufene Chargen (mit Restbestand)", "fr": "Lots expirés (avec stock restant)"},
    "Efficienza FEFO (First Expired First Out)": {"it": "Efficienza FEFO (First Expired First Out)", "en": "FEFO Efficiency (First Expired First Out)", "es": "Eficiencia FEFO (Primero en Caducar, Primero en Salir)", "de": "FEFO-Effizienz (First Expired First Out)", "fr": "Efficacité FEFO (Premier expiré, premier sorti)"},
    "Residuo": {"it": "Residuo", "en": "Remaining", "es": "Restante", "de": "Verbleibend", "fr": "Restant"},
    "Usato": {"it": "Usato", "en": "Used", "es": "Usado", "de": "Verwendet", "fr": "Utilisé"},
    "Perdita %": {"it": "Perdita %", "en": "Loss %", "es": "Pérdida %", "de": "Verlust %", "fr": "Perte %"},
    "Etichette Scaricate": {"it": "Etichette Scaricate", "en": "Unloaded Labels", "es": "Etiquetas Descargadas", "de": "Entladene Etiketten", "fr": "Étiquettes déchargées"},
    "FEFO Corrette": {"it": "FEFO Corrette", "en": "FEFO Correct", "es": "FEFO Correctas", "de": "FEFO korrekt", "fr": "FEFO Correct"},
    "Efficienza %": {"it": "Efficienza %", "en": "Efficiency %", "es": "Eficiencia %", "de": "Effizienz %", "fr": "Efficacité %"},
    "Lotti scaduti con giacenza:": {"it": "Lotti scaduti con giacenza:", "en": "Expired batches with stock:", "es": "Lotes caducados con existencias:", "de": "Abgelaufene Chargen mit Bestand:", "fr": "Lots expirés avec stock :"},
    "Etichette scadute (perdite):": {"it": "Etichette scadute (perdite):", "en": "Expired labels (losses):", "es": "Etiquetas caducadas (pérdidas):", "de": "Abgelaufene Etiketten (Verluste):", "fr": "Étiquettes expirées (pertes) :"},
    "In scadenza (30 gg):": {"it": "In scadenza (30 gg):", "en": "Expiring (30 days):", "es": "Por caducar (30 días):", "de": "Ablaufend (30 Tage):", "fr": "Expirant (30 jours) :"},
    "Analisi Fornitori": {"it": "Analisi Fornitori", "en": "Supplier Analysis", "es": "Análisis de Proveedores", "de": "Lieferantenanalyse", "fr": "Analyse fournisseurs"},
    "Ordini": {"it": "Ordini", "en": "Orders", "es": "Pedidos", "de": "Bestellungen", "fr": "Commandes"},
    "Ordinato": {"it": "Ordinato", "en": "Ordered", "es": "Pedido", "de": "Bestellt", "fr": "Commandé"},
    "Completamento %": {"it": "Completamento %", "en": "Completion %", "es": "Completado %", "de": "Fertigstellung %", "fr": "Achèvement %"},
    "TAT medio (gg)": {"it": "TAT medio (gg)", "en": "Avg TAT (days)", "es": "TAT promedio (días)", "de": "Durchschn. TAT (Tage)", "fr": "TAT moyen (jours)"},
    "Analisi Tempi (TAT)": {"it": "Analisi Tempi (TAT)", "en": "Time Analysis (TAT)", "es": "Análisis de Tiempos (TAT)", "de": "Zeitanalyse (TAT)", "fr": "Analyse des délais (TAT)"},
    "Metriche TAT": {"it": "Metriche TAT", "en": "TAT Metrics", "es": "Métricas TAT", "de": "TAT-Metriken", "fr": "Métriques TAT"},
    "Tempo Richiesta → Consegna (per fornitore)": {"it": "Tempo Richiesta → Consegna (per fornitore)", "en": "Request → Delivery Time (by supplier)", "es": "Tiempo Solicitud → Entrega (por proveedor)", "de": "Anfrage → Lieferzeit (nach Lieferant)", "fr": "Délai Demande → Livraison (par fournisseur)"},
    "Tempo in Magazzino (Carico → Scarico)": {"it": "Tempo in Magazzino (Carico → Scarico)", "en": "Warehouse Time (Load → Unload)", "es": "Tiempo en Almacén (Carga → Descarga)", "de": "Lagerzeit (Laden → Entladen)", "fr": "Temps en entrepôt (Chargement → Déchargement)"},
    "Media (gg)": {"it": "Media (gg)", "en": "Avg (days)", "es": "Promedio (días)", "de": "Durchschn. (Tage)", "fr": "Moy. (jours)"},
    "Min (gg)": {"it": "Min (gg)", "en": "Min (days)", "es": "Mín (días)", "de": "Min (Tage)", "fr": "Min (jours)"},
    "Max (gg)": {"it": "Max (gg)", "en": "Max (days)", "es": "Máx (días)", "de": "Max (Tage)", "fr": "Max (jours)"},
    "TAT medio ordini:": {"it": "TAT medio ordini:", "en": "Avg order TAT:", "es": "TAT promedio pedidos:", "de": "Durchschn. Bestell-TAT:", "fr": "TAT moyen commandes :"},
    "TAT medio magazzino:": {"it": "TAT medio magazzino:", "en": "Avg warehouse TAT:", "es": "TAT promedio almacén:", "de": "Durchschn. Lager-TAT:", "fr": "TAT moyen entrepôt :"},
    "giorni": {"it": "giorni", "en": "days", "es": "días", "de": "Tage", "fr": "jours"},
    "Analisi Consumi": {"it": "Analisi Consumi", "en": "Consumption Analysis", "es": "Análisis de Consumos", "de": "Verbrauchsanalyse", "fr": "Analyse de la consommation"},
    "Consumi per Prodotto": {"it": "Consumi per Prodotto", "en": "Consumption by Product", "es": "Consumos por Producto", "de": "Verbrauch nach Produkt", "fr": "Consommation par produit"},
    "Consumi per Categoria": {"it": "Consumi per Categoria", "en": "Consumption by Category", "es": "Consumos por Categoría", "de": "Verbrauch nach Kategorie", "fr": "Consommation par catégorie"},
    "Analisi Rotazione": {"it": "Analisi Rotazione", "en": "Rotation Analysis", "es": "Análisis de Rotación", "de": "Rotationsanalyse", "fr": "Analyse de rotation"},
    "Analisi Rotazione e ABC": {"it": "Analisi Rotazione e ABC", "en": "Rotation and ABC Analysis", "es": "Análisis de Rotación y ABC", "de": "Rotations- und ABC-Analyse", "fr": "Analyse rotation et ABC"},
    "Dashboard Statistiche": {"it": "Dashboard Statistiche", "en": "Statistics Dashboard", "es": "Panel de Estadísticas", "de": "Statistik-Dashboard", "fr": "Tableau de bord statistiques"},
    "Dashboard Magazzino": {"it": "Dashboard Magazzino", "en": "Warehouse Dashboard", "es": "Panel de Almacén", "de": "Lager-Dashboard", "fr": "Tableau de bord entrepôt"},
    "Sotto Soglia Riordino": {"it": "Sotto Soglia Riordino", "en": "Below Reorder Threshold", "es": "Bajo Umbral de Reorden", "de": "Unter Nachbestellgrenze", "fr": "Sous le seuil de réapprovisionnement"},
    "Movimenti (ultimi 30 giorni)": {"it": "Movimenti (ultimi 30 giorni)", "en": "Movements (last 30 days)", "es": "Movimientos (últimos 30 días)", "de": "Bewegungen (letzte 30 Tage)", "fr": "Mouvements (30 derniers jours)"},
    "Top 5 Consumi (30 giorni)": {"it": "Top 5 Consumi (30 giorni)", "en": "Top 5 Consumption (30 days)", "es": "Top 5 Consumos (30 días)", "de": "Top 5 Verbrauch (30 Tage)", "fr": "Top 5 consommation (30 jours)"},
    "Prodotti attivi:": {"it": "Prodotti attivi:", "en": "Active products:", "es": "Productos activos:", "de": "Aktive Produkte:", "fr": "Produits actifs :"},
    "Etichette in giacenza:": {"it": "Etichette in giacenza:", "en": "Labels in stock:", "es": "Etiquetas en existencia:", "de": "Etiketten im Bestand:", "fr": "Étiquettes en stock :"},
    "Lotti attivi:": {"it": "Lotti attivi:", "en": "Active batches:", "es": "Lotes activos:", "de": "Aktive Chargen:", "fr": "Lots actifs :"},
    "Prodotti sotto soglia:": {"it": "Prodotti sotto soglia:", "en": "Products below threshold:", "es": "Productos bajo umbral:", "de": "Produkte unter Grenze:", "fr": "Produits sous le seuil :"},
    "Prodotti esauriti:": {"it": "Prodotti esauriti:", "en": "Out of stock products:", "es": "Productos agotados:", "de": "Nicht vorrätige Produkte:", "fr": "Produits en rupture :"},
    "Lotti scaduti:": {"it": "Lotti scaduti:", "en": "Expired batches:", "es": "Lotes caducados:", "de": "Abgelaufene Chargen:", "fr": "Lots expirés :"},
    "In scadenza (60 gg):": {"it": "In scadenza (60 gg):", "en": "Expiring (60 days):", "es": "Por caducar (60 días):", "de": "Ablaufend (60 Tage):", "fr": "Expirant (60 jours) :"},
    "In scadenza (90 gg):": {"it": "In scadenza (90 gg):", "en": "Expiring (90 days):", "es": "Por caducar (90 días):", "de": "Ablaufend (90 Tage):", "fr": "Expirant (90 jours) :"},
    "Etichette caricate:": {"it": "Etichette caricate:", "en": "Labels loaded:", "es": "Etiquetas cargadas:", "de": "Etiketten geladen:", "fr": "Étiquettes chargées :"},
    "Etichette scaricate:": {"it": "Etichette scaricate:", "en": "Labels unloaded:", "es": "Etiquetas descargadas:", "de": "Etiketten entladen:", "fr": "Étiquettes déchargées :"},
    "Etichette annullate:": {"it": "Etichette annullate:", "en": "Labels cancelled:", "es": "Etiquetas canceladas:", "de": "Etiketten storniert:", "fr": "Étiquettes annulées :"},
    "Richieste aperte:": {"it": "Richieste aperte:", "en": "Open requests:", "es": "Solicitudes abiertas:", "de": "Offene Anfragen:", "fr": "Demandes ouvertes :"},
    "Articoli in attesa:": {"it": "Articoli in attesa:", "en": "Pending items:", "es": "Artículos pendientes:", "de": "Ausstehende Artikel:", "fr": "Articles en attente :"},
    "Nessun dato disponibile": {"it": "Nessun dato disponibile", "en": "No data available", "es": "Sin datos disponibles", "de": "Keine Daten verfügbar", "fr": "Aucune donnée disponible"},
    "Giacenza": {"it": "Giacenza", "en": "Stock", "es": "Existencias", "de": "Bestand", "fr": "Stock"},
    "Consumato": {"it": "Consumato", "en": "Consumed", "es": "Consumido", "de": "Verbraucht", "fr": "Consommé"},
    "Filtri": {"it": "Filtri", "en": "Filters", "es": "Filtros", "de": "Filter", "fr": "Filtres"},
    "Media/Mese": {"it": "Media/Mese", "en": "Avg/Month", "es": "Prom/Mes", "de": "Durchschn./Monat", "fr": "Moy./Mois"},
    "Totale prodotti": {"it": "Totale prodotti", "en": "Total products", "es": "Total productos", "de": "Produkte gesamt", "fr": "Total produits"},
    "Totale consumato": {"it": "Totale consumato", "en": "Total consumed", "es": "Total consumido", "de": "Gesamt verbraucht", "fr": "Total consommé"},
    "Periodo": {"it": "Periodo", "en": "Period", "es": "Período", "de": "Zeitraum", "fr": "Période"},
    "Esporta Consumi": {"it": "Esporta Consumi", "en": "Export Consumption", "es": "Exportar Consumos", "de": "Verbrauch exportieren", "fr": "Exporter consommation"},
    "60 gg": {"it": "60 gg", "en": "60 days", "es": "60 días", "de": "60 Tage", "fr": "60 jours"},
    "Classificazione ABC": {"it": "Classificazione ABC", "en": "ABC Classification", "es": "Clasificación ABC", "de": "ABC-Klassifizierung", "fr": "Classification ABC"},
    "Classificazione ABC:": {"it": "Classificazione ABC:", "en": "ABC Classification:", "es": "Clasificación ABC:", "de": "ABC-Klassifizierung:", "fr": "Classification ABC :"},
    "A = Alta rotazione (80% movimenti)": {"it": "A = Alta rotazione (80% movimenti)", "en": "A = High rotation (80% movements)", "es": "A = Alta rotación (80% movimientos)", "de": "A = Hohe Rotation (80% Bewegungen)", "fr": "A = Haute rotation (80% mouvements)"},
    "B = Media rotazione": {"it": "B = Media rotazione", "en": "B = Medium rotation", "es": "B = Media rotación", "de": "B = Mittlere Rotation", "fr": "B = Rotation moyenne"},
    "C = Bassa rotazione": {"it": "C = Bassa rotazione", "en": "C = Low rotation", "es": "C = Baja rotación", "de": "C = Niedrige Rotation", "fr": "C = Rotation faible"},
    "Copertura (gg)": {"it": "Copertura (gg)", "en": "Coverage (days)", "es": "Cobertura (días)", "de": "Reichweite (Tage)", "fr": "Couverture (jours)"},
    "ABC": {"it": "ABC", "en": "ABC", "es": "ABC", "de": "ABC", "fr": "ABC"},
    "Classe A": {"it": "Classe A", "en": "Class A", "es": "Clase A", "de": "Klasse A", "fr": "Classe A"},
    "Classe B": {"it": "Classe B", "en": "Class B", "es": "Clase B", "de": "Klasse B", "fr": "Classe B"},
    "Classe C": {"it": "Classe C", "en": "Class C", "es": "Clase C", "de": "Klasse C", "fr": "Classe C"},
    "Esporta Rotazione": {"it": "Esporta Rotazione", "en": "Export Rotation", "es": "Exportar Rotación", "de": "Rotation exportieren", "fr": "Exporter rotation"},
    "Classe": {"it": "Classe", "en": "Class", "es": "Clase", "de": "Klasse", "fr": "Classe"},
    "% Cumulativa": {"it": "% Cumulativa", "en": "Cumulative %", "es": "% Acumulado", "de": "Kumulativ %", "fr": "% Cumulé"},

    # ==========================================================================
    # Package history view
    # ==========================================================================
    "Storico Ordini": {"it": "Storico Ordini", "en": "Order History", "es": "Historial de Pedidos", "de": "Bestellverlauf", "fr": "Historique des commandes"},
    "Richiesta": {"it": "Richiesta", "en": "Request", "es": "Solicitud", "de": "Anfrage", "fr": "Demande"},
    "Data Richiesta": {"it": "Data Richiesta", "en": "Request Date", "es": "Fecha de Solicitud", "de": "Anfragedatum", "fr": "Date de demande"},
    "Qty Ordinata": {"it": "Qty Ordinata", "en": "Qty Ordered", "es": "Cant. Pedida", "de": "Bestellmenge", "fr": "Qté commandée"},
    "Qty Consegnata": {"it": "Qty Consegnata", "en": "Qty Delivered", "es": "Cant. Entregada", "de": "Liefermenge", "fr": "Qté livrée"},
    "Data Consegna": {"it": "Data Consegna", "en": "Delivery Date", "es": "Fecha de Entrega", "de": "Lieferdatum", "fr": "Date de livraison"},

    # ==========================================================================
    # Messages
    # ==========================================================================
    "Vuoi salvare?": {"it": "Vuoi salvare?", "en": "Do you want to save?", "es": "¿Desea guardar?", "de": "Möchten Sie speichern?", "fr": "Voulez-vous enregistrer ?"},
    "Operazione annullata.": {"it": "Operazione annullata.", "en": "Operation cancelled.", "es": "Operación cancelada.", "de": "Vorgang abgebrochen.", "fr": "Opération annulée."},
    "Seleziona un elemento!": {"it": "Seleziona un elemento!", "en": "Select an item!", "es": "¡Seleccione un elemento!", "de": "Artikel auswählen!", "fr": "Sélectionnez un élément !"},
    "Confermi eliminazione?": {"it": "Confermi eliminazione?", "en": "Confirm deletion?", "es": "¿Confirma eliminación?", "de": "Löschen bestätigen?", "fr": "Confirmer la suppression ?"},
    "Riavvio richiesto": {"it": "È necessario riavviare l'applicazione per applicare la nuova lingua.\n\nRiavviare ora?", "en": "Application restart is required to apply the new language.\n\nRestart now?", "es": "Es necesario reiniciar la aplicación para aplicar el nuevo idioma.\n\n¿Reiniciar ahora?", "de": "Application restart is required to apply the new language.\\n\\nRestart now?", "fr": "Application restart is required to apply the new language.\\n\\nRestart now?"},
    "Lingua cambiata": {"it": "Lingua cambiata", "en": "Language changed", "es": "Idioma cambiado", "de": "Sprache geändert", "fr": "Langue modifiée"},
    "Le date non sono valide!": {"it": "Le date non sono valide!", "en": "Dates are not valid!", "es": "¡Las fechas no son válidas!", "de": "Daten sind ungültig!", "fr": "Les dates ne sont pas valides !"},
    "Nessun dato nel periodo selezionato": {"it": "Nessun dato nel periodo selezionato", "en": "No data in selected period", "es": "Sin datos en el período seleccionado", "de": "Keine Daten im ausgewählten Zeitraum", "fr": "Aucune donnée dans la période sélectionnée"},
    "esiste già!": {"it": "esiste già!", "en": "already exists!", "es": "¡ya existe!", "de": "existiert bereits!", "fr": "existe déjà !"},
    "è già assegnato!": {"it": "è già assegnato!", "en": "is already assigned!", "es": "¡ya está asignado!", "de": "ist bereits zugewiesen!", "fr": "est déjà attribué !"},
    "Sì": {"it": "Sì", "en": "Yes", "es": "Sí", "de": "Ja", "fr": "Oui"},
    "No": {"it": "No", "en": "No", "es": "No", "de": "Nein", "fr": "Non"},

    # ==========================================================================
    # Menu - Purchases
    # ==========================================================================
    "Acquisti": {"it": "Acquisti", "en": "Purchases", "es": "Compras", "de": "Einkäufe", "fr": "Achats"},
    "Delibere": {"it": "Delibere", "en": "Deliberations", "es": "Deliberaciones", "de": "Beschlüsse", "fr": "Délibérations"},
    "Listino Prezzi": {"it": "Listino Prezzi", "en": "Price List", "es": "Lista de Precios", "de": "Preisliste", "fr": "Liste de prix"},
    "Fonti Package": {"it": "Fonti Package", "en": "Package Sources", "es": "Fuentes de Paquetes", "de": "Packungsquellen", "fr": "Sources de conditionnements"},
    "Fonti Finanziamento Packages": {"it": "Fonti Finanziamento Packages", "en": "Package Funding Sources", "es": "Fuentes de Financiación de Paquetes", "de": "Packungsfinanzierungsquellen", "fr": "Sources de financement des conditionnements"},

    # ==========================================================================
    # Deliberations view
    # ==========================================================================
    "Nuova Delibera": {"it": "Nuova Delibera", "en": "New Deliberation", "es": "Nueva Deliberación", "de": "Neuer Beschluss", "fr": "Nouvelle délibération"},
    "Modifica Delibera": {"it": "Modifica Delibera", "en": "Edit Deliberation", "es": "Editar Deliberación", "de": "Beschluss bearbeiten", "fr": "Modifier la délibération"},
    "Numero:": {"it": "Numero:", "en": "Number:", "es": "Número:", "de": "Nummer:", "fr": "Numéro :"},
    "Importo:": {"it": "Importo:", "en": "Amount:", "es": "Importe:", "de": "Betrag:", "fr": "Montant :"},
    "CIG:": {"it": "CIG:", "en": "CIG:", "es": "CIG:", "de": "CIG:", "fr": "CIG :"},
    "Attiva:": {"it": "Attiva:", "en": "Active:", "es": "Activa:", "de": "Aktiv:", "fr": "Actif :"},
    "Il campo Numero è obbligatorio!": {"it": "Il campo Numero è obbligatorio!", "en": "Number field is required!", "es": "¡El campo Número es obligatorio!", "de": "Nummer-Feld ist erforderlich!", "fr": "Le champ Numéro est requis !"},
    "Importo": {"it": "Importo", "en": "Amount", "es": "Importe", "de": "Betrag", "fr": "Montant"},
    "CIG": {"it": "CIG", "en": "CIG", "es": "CIG", "de": "CIG", "fr": "CIG"},
    "Delibera": {"it": "Delibera", "en": "Deliberation", "es": "Deliberación", "de": "Beschluss", "fr": "Délibération"},
    "Attive": {"it": "Attive", "en": "Active", "es": "Activas", "de": "Aktiv", "fr": "Actifs"},
    "Numero": {"it": "Numero", "en": "Number", "es": "Número", "de": "Nummer", "fr": "Numéro"},

    # ==========================================================================
    # Prices view
    # ==========================================================================
    "Nuovo Prezzo": {"it": "Nuovo Prezzo", "en": "New Price", "es": "Nuevo Precio", "de": "Neuer Preis", "fr": "Nouveau prix"},
    "Modifica Prezzo": {"it": "Modifica Prezzo", "en": "Edit Price", "es": "Editar Precio", "de": "Preis bearbeiten", "fr": "Modifier le prix"},
    "Prezzo:": {"it": "Prezzo:", "en": "Price:", "es": "Precio:", "de": "Preis:", "fr": "Prix :"},
    "Prezzo": {"it": "Prezzo", "en": "Price", "es": "Precio", "de": "Preis", "fr": "Prix"},
    "IVA %:": {"it": "IVA %:", "en": "VAT %:", "es": "IVA %:", "de": "MwSt. %:", "fr": "TVA % :"},
    "IVA %": {"it": "IVA %", "en": "VAT %", "es": "IVA %", "de": "MwSt. %", "fr": "TVA %"},
    "Valido dal:": {"it": "Valido dal:", "en": "Valid from:", "es": "Válido desde:", "de": "Gültig ab:", "fr": "Valide à partir de :"},
    "Valido dal": {"it": "Valido dal", "en": "Valid from", "es": "Válido desde", "de": "Gültig ab", "fr": "Valide à partir de"},
    "Il campo Prezzo è obbligatorio!": {"it": "Il campo Prezzo è obbligatorio!", "en": "Price field is required!", "es": "¡El campo Precio es obligatorio!", "de": "Preis-Feld ist erforderlich!", "fr": "Le champ Prix est requis !"},
    "Il campo Valido dal è obbligatorio!": {"it": "Il campo Valido dal è obbligatorio!", "en": "Valid from field is required!", "es": "¡El campo Válido desde es obligatorio!", "de": "Gültig ab-Feld ist erforderlich!", "fr": "Le champ Valide à partir de est requis !"},

    # ==========================================================================
    # Package fundings view
    # ==========================================================================
    "Nuova Fonte Finanziamento": {"it": "Nuova Fonte Finanziamento", "en": "New Funding Source", "es": "Nueva Fuente de Financiación", "de": "Neue Finanzierungsquelle", "fr": "Nouvelle source de financement"},
    "Modifica Fonte Finanziamento": {"it": "Modifica Fonte Finanziamento", "en": "Edit Funding Source", "es": "Editar Fuente de Financiación", "de": "Finanzierungsquelle bearbeiten", "fr": "Modifier la source de financement"},
    "Prodotto:": {"it": "Prodotto:", "en": "Product:", "es": "Producto:", "de": "Produkt:", "fr": "Produit :"},
    "Package:": {"it": "Package:", "en": "Package:", "es": "Paquete:", "de": "Packung:", "fr": "Conditionnement :"},
    "Fonte Finanziamento:": {"it": "Fonte Finanziamento:", "en": "Funding Source:", "es": "Fuente de Financiación:", "de": "Finanzierungsquelle:", "fr": "Source de financement :"},
    "Selezionare un Package!": {"it": "Selezionare un Package!", "en": "Select a Package!", "es": "¡Seleccione un Paquete!", "de": "Packung auswählen!", "fr": "Sélectionnez un conditionnement !"},
    "Selezionare una Fonte Finanziamento!": {"it": "Selezionare una Fonte Finanziamento!", "en": "Select a Funding Source!", "es": "¡Seleccione una Fuente de Financiación!", "de": "Finanzierungsquelle auswählen!", "fr": "Sélectionnez une source de financement !"},
    "Legenda": {"it": "Legenda", "en": "Legend", "es": "Leyenda", "de": "Legende", "fr": "Légende"},
    "In Gara": {"it": "In Gara", "en": "In Tender", "es": "En Licitación", "de": "In Ausschreibung", "fr": "En appel d'offres"},
    "Economia": {"it": "Economia", "en": "Direct Purchase", "es": "Compra Directa", "de": "Direktkauf", "fr": "Achat direct"},
    "(opzionale - se in gara)": {"it": "(opzionale - se in gara)", "en": "(optional - if in tender)", "es": "(opcional - si en licitación)", "de": "(optional - falls in Ausschreibung)", "fr": "(optionnel - si en appel d'offres)"},
    "Fonti/Delibere": {"it": "Fonti/Delibere", "en": "Sources/Delib.", "es": "Fuentes/Delib.", "de": "Quellen/Beschl.", "fr": "Sources/Délib."},
    "Cerca Package:": {"it": "Cerca Package:", "en": "Search Package:", "es": "Buscar Paquete:", "de": "Packung suchen:", "fr": "Rechercher conditionnement :"},
    "(descrizione o codice)": {"it": "(descrizione o codice)", "en": "(description or code)", "es": "(descripción o código)", "de": "(Beschreibung oder Code)", "fr": "(description ou code)"},
    "Risultati:": {"it": "Risultati:", "en": "Results:", "es": "Resultados:", "de": "Ergebnisse:", "fr": "Résultats :"},
    "Selezionato:": {"it": "Selezionato:", "en": "Selected:", "es": "Seleccionado:", "de": "Ausgewählt:", "fr": "Sélectionné :"},

    # ==========================================================================
    # Report Fundings
    # ==========================================================================
    "Report Fonti": {"it": "Report Fonti", "en": "Funding Report", "es": "Informe de Fuentes", "de": "Finanzierungsbericht", "fr": "Rapport de financement"},
    "Report Fonti Finanziamento": {"it": "Report Fonti Finanziamento", "en": "Funding Sources Report", "es": "Informe de Fuentes de Financiación", "de": "Finanzierungsquellenbericht", "fr": "Rapport des sources de financement"},
    "Nessun dato da esportare!": {"it": "Nessun dato da esportare!", "en": "No data to export!", "es": "¡No hay datos para exportar!", "de": "Keine Daten zum Exportieren!", "fr": "Aucune donnée à exporter !"},
    "File esportato": {"it": "File esportato", "en": "File exported", "es": "Archivo exportado", "de": "Datei exportiert", "fr": "Fichier exporté"},
    "Errore durante l'esportazione": {"it": "Errore durante l'esportazione", "en": "Error during export", "es": "Error durante la exportación", "de": "Fehler beim Exportieren", "fr": "Erreur lors de l'exportation"},
    "Errore durante esportazione": {"it": "Errore durante esportazione", "en": "Error during export", "es": "Error durante la exportación", "de": "Fehler beim Exportieren", "fr": "Erreur lors de l'exportation"},

    # ==========================================================================
    # Settings
    # ==========================================================================
    "Impostazioni Laboratorio": {"it": "Impostazioni Laboratorio", "en": "Laboratory Settings", "es": "Configuración del Laboratorio", "de": "Laboreinstellungen", "fr": "Paramètres du laboratoire"},
    "Ospedale:": {"it": "Ospedale:", "en": "Hospital:", "es": "Hospital:", "de": "Krankenhaus:", "fr": "Hôpital :"},
    "Laboratorio:": {"it": "Laboratorio:", "en": "Laboratory:", "es": "Laboratorio:", "de": "Labor:", "fr": "Laboratoire :"},
    "Responsabile:": {"it": "Responsabile:", "en": "Manager:", "es": "Responsable:", "de": "Leiter:", "fr": "Responsable :"},
    "Stanza/Locale:": {"it": "Stanza/Locale:", "en": "Room/Location:", "es": "Sala/Local:", "de": "Raum/Standort:", "fr": "Salle/Emplacement :"},
    "Telefono:": {"it": "Telefono:", "en": "Phone:", "es": "Teléfono:", "de": "Telefon:", "fr": "Téléphone :"},
    "IVA predefinita %:": {"it": "IVA predefinita %:", "en": "Default VAT %:", "es": "IVA predeterminado %:", "de": "Standard-MwSt. %:", "fr": "TVA par défaut % :"},
    "Timeout inattività (min):": {"it": "Timeout inattività (min):", "en": "Idle timeout (min):", "es": "Tiempo de espera inactivo (min):", "de": "Leerlauf-Timeout (Min.):", "fr": "Délai d'inactivité (min) :"},
    "(0 = disabilitato)": {"it": "(0 = disabilitato)", "en": "(0 = disabled)", "es": "(0 = deshabilitado)", "de": "(0 = deaktiviert)", "fr": "(0 = désactivé)"},
    "Impostazioni salvate.": {"it": "Impostazioni salvate.", "en": "Settings saved.", "es": "Configuración guardada.", "de": "Einstellungen gespeichert.", "fr": "Paramètres enregistrés."},
}


class I18N:
    """Internationalization helper class."""

    def __init__(self, language=None):
        """
        Initialize with specified language.

        Args:
            language: Language code ('it', 'en', 'es', 'de' or 'fr'). Defaults to DEFAULT_LANGUAGE.
        """
        self.language = language if language in LANGUAGES else DEFAULT_LANGUAGE

    def get(self, key):
        """
        Get translated string for key.

        Args:
            key: The string to translate (Italian version)

        Returns:
            Translated string, or key itself if not found
        """
        if key in TRANSLATIONS:
            return TRANSLATIONS[key].get(self.language, key)
        return key

    def __call__(self, key):
        """Shorthand for get()."""
        return self.get(key)

    def set_language(self, language):
        """
        Set current language.

        Args:
            language: Language code ('it', 'en', 'es', 'de' or 'fr')
        """
        if language in LANGUAGES:
            self.language = language

    @staticmethod
    def get_languages():
        """Return available languages."""
        return LANGUAGES.copy()


# Global instance - will be initialized by engine
_i18n = None


def get_translator():
    """Get global translator instance."""
    global _i18n
    if _i18n is None:
        _i18n = I18N()
    return _i18n


def set_language(language):
    """Set global language."""
    get_translator().set_language(language)


def _(key):
    """
    Translate a string using the global translator.

    This is the main function to use throughout the application.

    Args:
        key: String to translate (Italian version)

    Returns:
        Translated string
    """
    return get_translator().get(key)
