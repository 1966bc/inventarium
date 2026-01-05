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
DEFAULT_LANGUAGE = "en"

# Translation dictionary
TRANSLATIONS = {
    # ==========================================================================
    # Menu - File
    # ==========================================================================
    "File": {"it": "File", "en": "File", "es": "Archivo", "de": "Datei", "fr": "Fichier"},
    "Settings": {"it": "Impostazioni", "en": "Settings", "es": "Configuración", "de": "Einstellungen", "fr": "Paramètres"},
    "Configure Database": {"it": "Configura Database", "en": "Configure Database", "es": "Configurar Base de Datos", "de": "Datenbank konfigurieren", "fr": "Configurer la base de données"},
    "Database": {"it": "Database", "en": "Database", "es": "Base de Datos", "de": "Datenbank", "fr": "Base de données"},
    "Configure": {"it": "Configura", "en": "Configure", "es": "Configurar", "de": "Konfigurieren", "fr": "Configurer"},
    "Backup": {"it": "Backup", "en": "Backup", "es": "Copia de Seguridad", "de": "Sicherung", "fr": "Sauvegarde"},
    "Save Database Backup": {"it": "Salva Backup Database", "en": "Save Database Backup", "es": "Guardar Copia de Seguridad", "de": "Datenbanksicherung speichern", "fr": "Enregistrer la sauvegarde"},
    "Backup completed!": {"it": "Backup completato!", "en": "Backup completed!", "es": "¡Copia de seguridad completada!", "de": "Sicherung abgeschlossen!", "fr": "Sauvegarde terminée !"},
    "Error during backup:": {"it": "Errore durante il backup:", "en": "Error during backup:", "es": "Error durante la copia de seguridad:", "de": "Fehler bei der Sicherung:", "fr": "Erreur lors de la sauvegarde :"},
    "Compact": {"it": "Compatta", "en": "Compact", "es": "Compactar", "de": "Komprimieren", "fr": "Compacter"},
    "Backup Database": {"it": "Backup Database", "en": "Backup Database", "es": "Copia de Seguridad", "de": "Datenbank sichern", "fr": "Sauvegarder la base de données"},
    "Compact Database": {"it": "Compatta Database", "en": "Compact Database", "es": "Compactar Base de Datos", "de": "Datenbank komprimieren", "fr": "Compacter la base de données"},
    "Database compacted!": {"it": "Database compattato!", "en": "Database compacted!", "es": "¡Base de datos compactada!", "de": "Datenbank komprimiert!", "fr": "Base de données compactée !"},
    "Before": {"it": "Prima", "en": "Before", "es": "Antes", "de": "Vorher", "fr": "Avant"},
    "After": {"it": "Dopo", "en": "After", "es": "Después", "de": "Nachher", "fr": "Après"},
    "Saved": {"it": "Risparmiato", "en": "Saved", "es": "Ahorrado", "de": "Gespart", "fr": "Économisé"},
    "Error during compaction": {"it": "Errore durante la compattazione", "en": "Error during compaction", "es": "Error durante la compactación", "de": "Fehler beim Komprimieren", "fr": "Erreur lors du compactage"},
    "Database Configuration": {"it": "Configurazione Database", "en": "Database Configuration", "es": "Configuración de Base de Datos", "de": "Datenbankkonfiguration", "fr": "Configuration de la base de données"},
    "Configure Database Path": {"it": "Configura Percorso Database", "en": "Configure Database Path", "es": "Configurar Ruta de Base de Datos", "de": "Datenbankpfad konfigurieren", "fr": "Configurer le chemin de la base de données"},
    "Database path configuration.": {"it": "Configurazione del percorso database.", "en": "Database path configuration.", "es": "Configuración de la ruta de base de datos.", "de": "Datenbankpfad-Konfiguration.", "fr": "Configuration du chemin de la base de données."},
    "Select the SQLite database file (.db)": {"it": "Selezionare il file database SQLite (.db)", "en": "Select the SQLite database file (.db)", "es": "Seleccione el archivo de base de datos SQLite (.db)", "de": "SQLite-Datenbankdatei (.db) auswählen", "fr": "Sélectionnez le fichier de base de données SQLite (.db)"},
    "or enter the path manually.": {"it": "o inserire manualmente il percorso.", "en": "or enter the path manually.", "es": "o ingrese la ruta manualmente.", "de": "oder den Pfad manuell eingeben.", "fr": "ou entrez le chemin manuellement."},
    "Path:": {"it": "Percorso:", "en": "Path:", "es": "Ruta:", "de": "Pfad:", "fr": "Chemin :"},
    "Browse...": {"it": "Sfoglia...", "en": "Browse...", "es": "Examinar...", "de": "Durchsuchen...", "fr": "Parcourir..."},
    "Test Connection": {"it": "Test Connessione", "en": "Test Connection", "es": "Probar Conexión", "de": "Verbindung testen", "fr": "Tester la connexion"},
    "OK": {"it": "OK", "en": "OK", "es": "Aceptar", "de": "OK", "fr": "OK"},
    "Enter a path": {"it": "Inserire un percorso", "en": "Enter a path", "es": "Ingrese una ruta", "de": "Pfad eingeben", "fr": "Entrez un chemin"},
    "File not found": {"it": "File non trovato", "en": "File not found", "es": "Archivo no encontrado", "de": "Datei nicht gefunden", "fr": "Fichier non trouvé"},
    "Invalid database": {"it": "Database non valido", "en": "Invalid database", "es": "Base de datos no válida", "de": "Ungültige Datenbank", "fr": "Base de données invalide"},
    "products found": {"it": "prodotti trovati", "en": "products found", "es": "productos encontrados", "de": "Produkte gefunden", "fr": "produits trouvés"},
    "Error": {"it": "Errore", "en": "Error", "es": "Error", "de": "Fehler", "fr": "Erreur"},
    "Select Database": {"it": "Seleziona Database", "en": "Select Database", "es": "Seleccionar Base de Datos", "de": "Datenbank auswählen", "fr": "Sélectionner la base de données"},
    "All files": {"it": "Tutti i file", "en": "All files", "es": "Todos los archivos", "de": "Alle Dateien", "fr": "Tous les fichiers"},
    "Configuration": {"it": "Configurazione", "en": "Configuration", "es": "Configuración", "de": "Konfiguration", "fr": "Configuration"},
    "Enter a valid path.": {"it": "Inserire un percorso valido.", "en": "Enter a valid path.", "es": "Ingrese una ruta válida.", "de": "Gültigen Pfad eingeben.", "fr": "Entrez un chemin valide."},
    "File does not exist:": {"it": "Il file non esiste:", "en": "File does not exist:", "es": "El archivo no existe:", "de": "Datei existiert nicht:", "fr": "Le fichier n'existe pas :"},
    "Continue anyway?": {"it": "Continuare comunque?", "en": "Continue anyway?", "es": "¿Continuar de todos modos?", "de": "Trotzdem fortfahren?", "fr": "Continuer quand même ?"},
    "Database path updated.": {"it": "Percorso database aggiornato.", "en": "Database path updated.", "es": "Ruta de base de datos actualizada.", "de": "Datenbankpfad aktualisiert.", "fr": "Chemin de la base de données mis à jour."},
    "Restart the application to use the new database.": {"it": "Riavviare l'applicazione per utilizzare il nuovo database.", "en": "Restart the application to use the new database.", "es": "Reinicie la aplicación para usar la nueva base de datos.", "de": "Anwendung neu starten, um die neue Datenbank zu verwenden.", "fr": "Redémarrez l'application pour utiliser la nouvelle base de données."},
    "Restart now?": {"it": "Riavviare ora?", "en": "Restart now?", "es": "¿Reiniciar ahora?", "de": "Jetzt neu starten?", "fr": "Redémarrer maintenant ?"},
    "Database not found.": {"it": "Database non trovato.", "en": "Database not found.", "es": "Base de datos no encontrada.", "de": "Datenbank nicht gefunden.", "fr": "Base de données non trouvée."},
    "What do you want to do?": {"it": "Cosa vuoi fare?", "en": "What do you want to do?", "es": "¿Qué quieres hacer?", "de": "Was möchten Sie tun?", "fr": "Que voulez-vous faire ?"},
    "Find existing database...": {"it": "Cerca database esistente...", "en": "Find existing database...", "es": "Buscar base de datos existente...", "de": "Vorhandene Datenbank suchen...", "fr": "Rechercher une base de données existante..."},
    "Create new database": {"it": "Crea nuovo database", "en": "Create new database", "es": "Crear nueva base de datos", "de": "Neue Datenbank erstellen", "fr": "Créer une nouvelle base de données"},
    "Create New Database": {"it": "Crea Nuovo Database", "en": "Create New Database", "es": "Crear Nueva Base de Datos", "de": "Neue Datenbank erstellen", "fr": "Créer une nouvelle base de données"},
    "Database Created": {"it": "Database Creato", "en": "Database Created", "es": "Base de Datos Creada", "de": "Datenbank erstellt", "fr": "Base de données créée"},
    "Database created successfully!": {"it": "Database creato con successo!", "en": "Database created successfully!", "es": "¡Base de datos creada con éxito!", "de": "Datenbank erfolgreich erstellt!", "fr": "Base de données créée avec succès !"},
    "Unable to create database.": {"it": "Impossibile creare il database.", "en": "Unable to create database.", "es": "No se puede crear la base de datos.", "de": "Datenbank kann nicht erstellt werden.", "fr": "Impossible de créer la base de données."},
    "The selected file is not a valid Inventarium database.": {"it": "Il file selezionato non è un database Inventarium valido.", "en": "The selected file is not a valid Inventarium database.", "es": "El archivo seleccionado no es una base de datos Inventarium válida.", "de": "Die ausgewählte Datei ist keine gültige Inventarium-Datenbank.", "fr": "Le fichier sélectionné n'est pas une base de données Inventarium valide."},
    "File init.sql not found!": {"it": "File init.sql non trovato!", "en": "File init.sql not found!", "es": "¡Archivo init.sql no encontrado!", "de": "Datei init.sql nicht gefunden!", "fr": "Fichier init.sql non trouvé !"},
    "Error creating database:": {"it": "Errore durante la creazione del database:", "en": "Error creating database:", "es": "Error al crear la base de datos:", "de": "Fehler beim Erstellen der Datenbank:", "fr": "Erreur lors de la création de la base de données :"},
    "Log": {"it": "Log", "en": "Log", "es": "Registro", "de": "Protokoll", "fr": "Journal"},
    "Custom Label": {"it": "Etichetta Personalizzata", "en": "Custom Label", "es": "Etiqueta Personalizada", "de": "Benutzerdefiniertes Etikett", "fr": "Étiquette personnalisée"},
    "Exit": {"it": "Esci", "en": "Exit", "es": "Salir", "de": "Beenden", "fr": "Quitter"},
    "Do you want to quit Inventarium?": {"it": "Vuoi uscire da Inventarium?", "en": "Do you want to quit Inventarium?", "es": "¿Desea salir de Inventarium?", "de": "Möchten Sie Inventarium beenden?", "fr": "Voulez-vous quitter Inventarium ?"},
    "Fatal error:": {"it": "Errore fatale:", "en": "Fatal error:", "es": "Error fatal:", "de": "Schwerwiegender Fehler:", "fr": "Erreur fatale :"},
    "Language": {"it": "Lingua", "en": "Language", "es": "Idioma", "de": "Sprache", "fr": "Langue"},

    # ==========================================================================
    # Menu - Warehouse
    # ==========================================================================
    "Warehouse": {"it": "Magazzino", "en": "Warehouse", "es": "Almacén", "de": "Lager", "fr": "Entrepôt"},
    "Stock": {"it": "Giacenze", "en": "Stock", "es": "Existencias", "de": "Bestand", "fr": "Stock"},
    "Print Stock": {"it": "Stampa Giacenze", "en": "Print Stock", "es": "Imprimir Existencias", "de": "Bestand drucken", "fr": "Imprimer le stock"},
    "Unload": {"it": "Scarico", "en": "Unload", "es": "Descarga", "de": "Entladen", "fr": "Décharger"},
    "Expiring": {"it": "Scadenze", "en": "Expiring", "es": "Caducidades", "de": "Ablaufend", "fr": "Expirations"},

    # ==========================================================================
    # Menu - Requests
    # ==========================================================================
    "Requests": {"it": "Richieste", "en": "Requests", "es": "Solicitudes", "de": "Anfragen", "fr": "Demandes"},
    "Deliveries": {"it": "Consegne", "en": "Deliveries", "es": "Entregas", "de": "Lieferungen", "fr": "Livraisons"},

    # ==========================================================================
    # Menu - Admin
    # ==========================================================================
    "Master Data": {"it": "Anagrafiche", "en": "Master Data", "es": "Datos Maestros", "de": "Stammdaten", "fr": "Données de base"},
    "Products": {"it": "Prodotti", "en": "Products", "es": "Productos", "de": "Produkte", "fr": "Produits"},
    "Suppliers": {"it": "Fornitori", "en": "Suppliers", "es": "Proveedores", "de": "Lieferanten", "fr": "Fournisseurs"},
    "Categories": {"it": "Categorie", "en": "Categories", "es": "Categorías", "de": "Kategorien", "fr": "Catégories"},
    "Storage Conditions": {"it": "Conservazioni", "en": "Storage Conditions", "es": "Condiciones de Almacenamiento", "de": "Lagerbedingungen", "fr": "Conditions de stockage"},
    "Locations": {"it": "Ubicazioni", "en": "Locations", "es": "Ubicaciones", "de": "Standorte", "fr": "Emplacements"},
    "Funding Sources": {"it": "Fonti Finanziamento", "en": "Funding Sources", "es": "Fuentes de Financiación", "de": "Finanzierungsquellen", "fr": "Sources de financement"},
    "Funding Sources": {"it": "Fonti di Finanziamento", "en": "Funding Sources", "es": "Fuentes de Financiación", "de": "Finanzierungsquellen", "fr": "Sources de financement"},
    "Total": {"it": "Totale", "en": "Total", "es": "Total", "de": "Gesamt", "fr": "Total"},

    # ==========================================================================
    # Menu - Statistics
    # ==========================================================================
    "Statistics": {"it": "Statistiche", "en": "Statistics", "es": "Estadísticas", "de": "Statistiken", "fr": "Statistiques"},
    "Dashboard": {"it": "Dashboard", "en": "Dashboard", "es": "Panel de Control", "de": "Dashboard", "fr": "Tableau de bord"},
    "Consumption": {"it": "Consumi", "en": "Consumption", "es": "Consumos", "de": "Verbrauch", "fr": "Consommation"},
    "Rotation": {"it": "Rotazione", "en": "Rotation", "es": "Rotación", "de": "Rotation", "fr": "Rotation"},
    "Times (TAT)": {"it": "Tempi (TAT)", "en": "Times (TAT)", "es": "Tiempos (TAT)", "de": "Zeiten (TAT)", "fr": "Délais (TAT)"},

    # ==========================================================================
    # Menu - Help
    # ==========================================================================
    "About": {"it": "Informazioni", "en": "About", "es": "Acerca de", "de": "Über", "fr": "À propos"},
    "License": {"it": "Licenza", "en": "License", "es": "Licencia", "de": "Lizenz", "fr": "Licence"},
    "Python Version": {"it": "Versione Python", "en": "Python Version", "es": "Versión de Python", "de": "Python-Version", "fr": "Version Python"},
    "Tkinter Version": {"it": "Versione Tkinter", "en": "Tkinter Version", "es": "Versión de Tkinter", "de": "Tkinter-Version", "fr": "Version Tkinter"},

    # ==========================================================================
    # Common buttons
    # ==========================================================================
    "Save": {"it": "Salva", "en": "Save", "es": "Guardar", "de": "Speichern", "fr": "Enregistrer"},
    "Close": {"it": "Chiudi", "en": "Close", "es": "Cerrar", "de": "Schließen", "fr": "Fermer"},
    "Cancel": {"it": "Annulla", "en": "Cancel", "es": "Cancelar", "de": "Abbrechen", "fr": "Annuler"},
    "New": {"it": "Nuovo", "en": "New", "es": "Nuevo", "de": "Neu", "fr": "Nouveau"},
    "Edit": {"it": "Modifica", "en": "Edit", "es": "Editar", "de": "Bearbeiten", "fr": "Modifier"},
    "Delete": {"it": "Elimina", "en": "Delete", "es": "Eliminar", "de": "Löschen", "fr": "Supprimer"},
    "Search": {"it": "Cerca", "en": "Search", "es": "Buscar", "de": "Suchen", "fr": "Rechercher"},
    "Copied!": {"it": "Copiato!", "en": "Copied!", "es": "¡Copiado!", "de": "Kopiert!", "fr": "Copié !"},
    "Refresh": {"it": "Aggiorna", "en": "Refresh", "es": "Actualizar", "de": "Aktualisieren", "fr": "Actualiser"},
    "Print": {"it": "Stampa", "en": "Print", "es": "Imprimir", "de": "Drucken", "fr": "Imprimer"},
    "Export CSV": {"it": "Esporta CSV", "en": "Export CSV", "es": "Exportar CSV", "de": "CSV exportieren", "fr": "Exporter CSV"},
    "Unload": {"it": "Scarica", "en": "Unload", "es": "Descargar", "de": "Entladen", "fr": "Décharger"},
    "Cancel Batch": {"it": "Annulla Lotto", "en": "Cancel Batch", "es": "Cancelar Lote", "de": "Charge stornieren", "fr": "Annuler le lot"},
    "Calculate": {"it": "Calcola", "en": "Calculate", "es": "Calcular", "de": "Berechnen", "fr": "Calculer"},
    "Load": {"it": "Carica", "en": "Load", "es": "Cargar", "de": "Laden", "fr": "Charger"},
    "Preview": {"it": "Anteprima", "en": "Preview", "es": "Vista Previa", "de": "Vorschau", "fr": "Aperçu"},
    "Details": {"it": "Dettagli", "en": "Details", "es": "Detalles", "de": "Details", "fr": "Détails"},
    "History": {"it": "Storico", "en": "History", "es": "Historial", "de": "Verlauf", "fr": "Historique"},
    "New Batch": {"it": "Nuovo Lotto", "en": "New Batch", "es": "Nuevo Lote", "de": "Neue Charge", "fr": "Nouveau lot"},
    "Load Labels": {"it": "Carica Etichette", "en": "Load Labels", "es": "Cargar Etiquetas", "de": "Etiketten laden", "fr": "Charger les étiquettes"},
    "Packages": {"it": "Confezioni", "en": "Packages", "es": "Envases", "de": "Packungen", "fr": "Conditionnements"},
    "Generate": {"it": "Genera", "en": "Generate", "es": "Generar", "de": "Generieren", "fr": "Générer"},

    # ==========================================================================
    # Package History
    # ==========================================================================
    "Order History": {"it": "Storico Ordini", "en": "Order History", "es": "Historial de Pedidos", "de": "Bestellverlauf", "fr": "Historique des commandes"},
    "Date": {"it": "Data", "en": "Date", "es": "Fecha", "de": "Datum", "fr": "Date"},
    "Request Ref.": {"it": "Rif. Richiesta", "en": "Request Ref.", "es": "Ref. Solicitud", "de": "Anfrage-Ref.", "fr": "Réf. demande"},
    "Ord.": {"it": "Ord.", "en": "Ord.", "es": "Ped.", "de": "Best.", "fr": "Com."},
    "Deliv.": {"it": "Evaso", "en": "Deliv.", "es": "Entr.", "de": "Lief.", "fr": "Livré"},
    "Rows": {"it": "Righe", "en": "Rows", "es": "Filas", "de": "Zeilen", "fr": "Lignes"},
    "Tot. Ord": {"it": "Tot. Ord", "en": "Tot. Ord", "es": "Tot. Ped", "de": "Ges. Best.", "fr": "Tot. Com."},
    "Tot. Deliv": {"it": "Tot. Evaso", "en": "Tot. Deliv", "es": "Tot. Entr", "de": "Ges. Lief.", "fr": "Tot. Livré"},

    # ==========================================================================
    # Batch Dialog
    # ==========================================================================
    "Edit Batch": {"it": "Modifica Lotto", "en": "Edit Batch", "es": "Editar Lote", "de": "Charge bearbeiten", "fr": "Modifier le lot"},
    "The Expiration date is not valid!": {"it": "La data Scadenza non è valida!", "en": "The Expiration date is not valid!", "es": "¡La fecha de Vencimiento no es válida!", "de": "Das Ablaufdatum ist ungültig!", "fr": "La date d'expiration n'est pas valide !"},
    "Il lotto '{}' con scadenza {} esiste già!": {"it": "Il lotto '{}' con scadenza {} esiste già!", "en": "Batch '{}' with expiration {} already exists!", "es": "¡El lote '{}' con vencimiento {} ya existe!", "de": "Charge '{}' mit Ablauf {} existiert bereits!", "fr": "Le lot '{}' avec expiration {} existe déjà !"},
    "Il lotto '{}' esiste già con scadenza {}.\nVuoi inserirlo comunque con scadenza {}?": {"it": "Il lotto '{}' esiste già con scadenza {}.\nVuoi inserirlo comunque con scadenza {}?", "en": "Batch '{}' already exists with expiration {}.\nInsert anyway with expiration {}?", "es": "El lote '{}' ya existe con vencimiento {}.\n¿Insertar de todos modos con vencimiento {}?", "de": "Batch '{}' already exists with expiration {}.\\nInsert anyway with expiration {}?", "fr": "Batch '{}' already exists with expiration {}.\\nInsert anyway with expiration {}?"},
    "The batch is already expired!\nCannot insert.": {"it": "Il lotto è già scaduto!\nImpossibile inserire.", "en": "The batch is already expired!\nCannot insert.", "es": "¡El lote ya está vencido!\nNo se puede insertar.", "de": "The batch is already expired!\\nCannot insert.", "fr": "The batch is already expired!\\nCannot insert."},
    "Attenzione: il lotto scade tra {} giorni.\nProcedere comunque?": {"it": "Attenzione: il lotto scade tra {} giorni.\nProcedere comunque?", "en": "Warning: batch expires in {} days.\nProceed anyway?", "es": "Advertencia: el lote vence en {} días.\n¿Continuar de todos modos?", "de": "Warning: batch expires in {} days.\\nProceed anyway?", "fr": "Warning: batch expires in {} days.\\nProceed anyway?"},

    # ==========================================================================
    # Custom Label
    # ==========================================================================
    "Line 1:": {"it": "Riga 1:", "en": "Line 1:", "es": "Línea 1:", "de": "Zeile 1:", "fr": "Ligne 1 :"},
    "Line 2:": {"it": "Riga 2:", "en": "Line 2:", "es": "Línea 2:", "de": "Zeile 2:", "fr": "Ligne 2 :"},
    "Line 3:": {"it": "Riga 3:", "en": "Line 3:", "es": "Línea 3:", "de": "Zeile 3:", "fr": "Ligne 3 :"},
    "Font Size:": {"it": "Dim. Font:", "en": "Font Size:", "es": "Tam. Fuente:", "de": "Schriftgröße:", "fr": "Taille police :"},
    "Custom Label": {"it": "Etichetta Personalizzata", "en": "Custom Label", "es": "Etiqueta Personalizada", "de": "Benutzerdefiniertes Etikett", "fr": "Étiquette personnalisée"},
    "Error saving templates:": {"it": "Errore nel salvare i modelli:", "en": "Error saving templates:", "es": "Error al guardar plantillas:", "de": "Fehler beim Speichern der Vorlagen:", "fr": "Erreur lors de l'enregistrement des modèles :"},
    "Enter at least the first line!": {"it": "Inserire almeno la prima riga!", "en": "Enter at least the first line!", "es": "¡Ingrese al menos la primera línea!", "de": "Mindestens die erste Zeile eingeben!", "fr": "Entrez au moins la première ligne !"},
    "Il modello '{}' esiste.\nSovrascrivere?": {"it": "Il modello '{}' esiste.\nSovrascrivere?", "en": "Template '{}' exists.\nOverwrite?", "es": "La plantilla '{}' existe.\n¿Sobrescribir?", "de": "Template '{}' exists.\\nOverwrite?", "fr": "Template '{}' exists.\\nOverwrite?"},
    "Modello '{}' salvato!": {"it": "Modello '{}' salvato!", "en": "Template '{}' saved!", "es": "¡Plantilla '{}' guardada!", "de": "Vorlage '{}' gespeichert!", "fr": "Modèle '{}' enregistré !"},
    "Eliminare il modello '{}'?": {"it": "Eliminare il modello '{}'?", "en": "Delete template '{}'?", "es": "¿Eliminar plantilla '{}'?", "de": "Vorlage '{}' löschen?", "fr": "Supprimer le modèle '{}' ?"},
    "Enter at least one line of text!": {"it": "Inserire almeno una riga di testo!", "en": "Enter at least one line of text!", "es": "¡Ingrese al menos una línea de texto!", "de": "Mindestens eine Textzeile eingeben!", "fr": "Entrez au moins une ligne de texte !"},
    "Error in generation:": {"it": "Errore nella generazione:", "en": "Error in generation:", "es": "Error en la generación:", "de": "Fehler bei der Generierung:", "fr": "Erreur lors de la génération :"},
    "Label sent to print!": {"it": "Etichetta inviata alla stampa!", "en": "Label sent to print!", "es": "¡Etiqueta enviada a imprimir!", "de": "Etikett zum Drucken gesendet!", "fr": "Étiquette envoyée à l'impression !"},
    "Error in printing:": {"it": "Errore nella stampa:", "en": "Error in printing:", "es": "Error en la impresión:", "de": "Fehler beim Drucken:", "fr": "Erreur lors de l'impression :"},

    # ==========================================================================
    # Expiring Batches
    # ==========================================================================
    "Days Exp.": {"it": "GG Scad.", "en": "Days Exp.", "es": "Días Venc.", "de": "Tage Abl.", "fr": "Jours Exp."},
    "Stock": {"it": "Giac.", "en": "Stock", "es": "Stock", "de": "Bestand", "fr": "Stock"},
    "Expiring Batches (30 days)": {"it": "Lotti in Scadenza (30 giorni)", "en": "Expiring Batches (30 days)", "es": "Lotes por Vencer (30 días)", "de": "Ablaufende Chargen (30 Tage)", "fr": "Lots expirants (30 jours)"},
    "Days Left": {"it": "GG Rim.", "en": "Days Left", "es": "Días Rest.", "de": "Tage übrig", "fr": "Jours rest."},
    "Select an expired batch to cancel!": {"it": "Seleziona un lotto scaduto da annullare!", "en": "Select an expired batch to cancel!", "es": "¡Seleccione un lote vencido para cancelar!", "de": "Abgelaufene Charge zum Stornieren auswählen!", "fr": "Sélectionnez un lot expiré à annuler !"},
    "Annullare il lotto '{}' di '{}'?\n\nVerranno annullate {} etichette in giacenza.\n\nQuesta operazione non è reversibile.": {"it": "Annullare il lotto '{}' di '{}'?\n\nVerranno annullate {} etichette in giacenza.\n\nQuesta operazione non è reversibile.", "en": "Cancel batch '{}' of '{}'?\n\n{} labels in stock will be cancelled.\n\nThis operation is not reversible.", "es": "¿Cancelar lote '{}' de '{}'?\n\nSe cancelarán {} etiquetas en stock.\n\nEsta operación no es reversible.", "de": "Cancel batch '{}' of '{}'?\\n\\n{} labels in stock will be cancelled.\\n\\nThis operation is not reversible.", "fr": "Cancel batch '{}' of '{}'?\\n\\n{} labels in stock will be cancelled.\\n\\nThis operation is not reversible."},
    "Lotto '{}' annullato con successo.": {"it": "Lotto '{}' annullato con successo.", "en": "Batch '{}' cancelled successfully.", "es": "Lote '{}' cancelado exitosamente.", "de": "Charge '{}' erfolgreich storniert.", "fr": "Lot '{}' annulé avec succès."},

    # ==========================================================================
    # Labels Dialog
    # ==========================================================================
    "Product:": {"it": "Prodotto:", "en": "Product:", "es": "Producto:", "de": "Produkt:", "fr": "Produit :"},
    "Number of labels:": {"it": "Numero etichette:", "en": "Number of labels:", "es": "Número de etiquetas:", "de": "Anzahl Etiketten:", "fr": "Nombre d'étiquettes :"},
    "Enter a valid number of labels!": {"it": "Inserire un numero di etichette valido!", "en": "Enter a valid number of labels!", "es": "¡Ingrese un número de etiquetas válido!", "de": "Gültige Anzahl Etiketten eingeben!", "fr": "Entrez un nombre d'étiquettes valide !"},
    "Caricare {} etichetta?": {"it": "Caricare {} etichetta?", "en": "Load {} label?", "es": "¿Cargar {} etiqueta?", "de": "{} Etikett laden?", "fr": "Charger {} étiquette ?"},
    "Caricare {} etichette?": {"it": "Caricare {} etichette?", "en": "Load {} labels?", "es": "¿Cargar {} etiquetas?", "de": "{} Etiketten laden?", "fr": "Charger {} étiquettes ?"},

    # ==========================================================================
    # Locations
    # ==========================================================================
    "Type:": {"it": "Tipo:", "en": "Type:", "es": "Tipo:", "de": "Typ:", "fr": "Type :"},
    "-- Not assigned --": {"it": "-- Non assegnato --", "en": "-- Not assigned --", "es": "-- No asignado --", "de": "-- Nicht zugewiesen --", "fr": "-- Non assigné --"},
    "Room": {"it": "Stanza", "en": "Room", "es": "Sala", "de": "Raum", "fr": "Salle"},
    "Storage": {"it": "Conserv.", "en": "Storage", "es": "Conserv.", "de": "Lagerung", "fr": "Stockage"},
    "Select location:": {"it": "Seleziona ubicazione:", "en": "Select location:", "es": "Seleccionar ubicación:", "de": "Standort auswählen:", "fr": "Sélectionner l'emplacement :"},

    # ==========================================================================
    # Packages
    # ==========================================================================
    "Suppl.Code": {"it": "Cod.Forn.", "en": "Suppl.Code", "es": "Cód.Prov.", "de": "Lief.Code", "fr": "Code fourn."},
    "Lab.": {"it": "Et.", "en": "Lab.", "es": "Et.", "de": "Et.", "fr": "Ét."},
    "D": {"it": "B", "en": "D", "es": "O", "de": "D", "fr": "O"},

    # ==========================================================================
    # Report Fundings
    # ==========================================================================
    "Tender:": {"it": "In Gara:", "en": "Tender:", "es": "Licitación:", "de": "Ausschreibung:", "fr": "Appel d'offres :"},
    "Budget:": {"it": "Economia:", "en": "Budget:", "es": "Presupuesto:", "de": "Budget:", "fr": "Budget :"},

    # ==========================================================================
    # Requests
    # ==========================================================================
    "It.": {"it": "Art.", "en": "It.", "es": "Art.", "de": "Art.", "fr": "Art."},
    "Pack.": {"it": "Conf.", "en": "Pack.", "es": "Conf.", "de": "Pack.", "fr": "Cond."},
    "Qty": {"it": "Qtà", "en": "Qty", "es": "Cant.", "de": "Menge", "fr": "Qté"},

    # ==========================================================================
    # Warehouse
    # ==========================================================================
    "S.": {"it": "G.", "en": "S.", "es": "S.", "de": "B.", "fr": "S."},
    "Days": {"it": "GG", "en": "Days", "es": "Días", "de": "Tage", "fr": "Jours"},

    # ==========================================================================
    # Statistics
    # ==========================================================================
    "Loss %": {"it": "Perdita %", "en": "Loss %", "es": "Pérdida %", "de": "Verlust %", "fr": "Perte %"},
    "Efficiency %": {"it": "Efficienza %", "en": "Efficiency %", "es": "Eficiencia %", "de": "Effizienz %", "fr": "Efficacité %"},
    "Completion %": {"it": "Completamento %", "en": "Completion %", "es": "Completado %", "de": "Fertigstellung %", "fr": "Achèvement %"},
    "Avg TAT (days)": {"it": "TAT medio (gg)", "en": "Avg TAT (days)", "es": "TAT medio (días)", "de": "Durchschn. TAT (Tage)", "fr": "TAT moyen (jours)"},
    "Avg (days)": {"it": "Media (gg)", "en": "Avg (days)", "es": "Media (días)", "de": "Durchschn. (Tage)", "fr": "Moy. (jours)"},
    "Min (days)": {"it": "Min (gg)", "en": "Min (days)", "es": "Mín (días)", "de": "Min (Tage)", "fr": "Min (jours)"},
    "Max (days)": {"it": "Max (gg)", "en": "Max (days)", "es": "Máx (días)", "de": "Max (Tage)", "fr": "Max (jours)"},

    # ==========================================================================
    # Common labels
    # ==========================================================================
    "Description:": {"it": "Descrizione:", "en": "Description:", "es": "Descripción:", "de": "Beschreibung:", "fr": "Description :"},
    "Code:": {"it": "Codice:", "en": "Code:", "es": "Código:", "de": "Code:", "fr": "Code :"},
    "Active:": {"it": "Attivo:", "en": "Active:", "es": "Activo:", "de": "Aktiv:", "fr": "Actif :"},
    "Status": {"it": "Stato", "en": "Status", "es": "Estado", "de": "Status", "fr": "Statut"},
    "Active": {"it": "Attivi", "en": "Active", "es": "Activos", "de": "Aktiv", "fr": "Actifs"},
    "Inactive": {"it": "Non Attivi", "en": "Inactive", "es": "Inactivos", "de": "Inaktiv", "fr": "Inactifs"},
    "All": {"it": "Tutti", "en": "All", "es": "Todos", "de": "Alle", "fr": "Tous"},
    "Search": {"it": "Ricerca", "en": "Search", "es": "Búsqueda", "de": "Suchen", "fr": "Rechercher"},
    "Total:": {"it": "Totale:", "en": "Total:", "es": "Total:", "de": "Gesamt:", "fr": "Total :"},
    "From:": {"it": "Da:", "en": "From:", "es": "Desde:", "de": "Von:", "fr": "De :"},
    "To:": {"it": "A:", "en": "To:", "es": "Hasta:", "de": "Bis:", "fr": "À :"},
    "Quick period:": {"it": "Periodo rapido:", "en": "Quick period:", "es": "Período rápido:", "de": "Schnellauswahl:", "fr": "Période rapide :"},
    "Type": {"it": "Tipo", "en": "Type", "es": "Tipo", "de": "Typ", "fr": "Type"},
    "Description": {"it": "Descrizione", "en": "Description", "es": "Descripción", "de": "Beschreibung", "fr": "Description"},
    "Code": {"it": "Codice", "en": "Code", "es": "Código", "de": "Code", "fr": "Code"},

    # ==========================================================================
    # Warehouse view
    # ==========================================================================
    "Product": {"it": "Prodotto", "en": "Product", "es": "Producto", "de": "Produkt", "fr": "Produit"},
    "Batch": {"it": "Lotto", "en": "Batch", "es": "Lote", "de": "Charge", "fr": "Lot"},
    "Batches": {"it": "Lotti", "en": "Batches", "es": "Lotes", "de": "Chargen", "fr": "Lots"},
    "Expiration": {"it": "Scadenza", "en": "Expiration", "es": "Caducidad", "de": "Ablauf", "fr": "Expiration"},
    "Labels": {"it": "Etichette", "en": "Labels", "es": "Etiquetas", "de": "Etiketten", "fr": "Étiquettes"},
    "Label action": {"it": "Azione etichetta", "en": "Label action", "es": "Acción de etiqueta", "de": "Etikett-Aktion", "fr": "Action étiquette"},
    "Dispatch": {"it": "Evadi", "en": "Dispatch", "es": "Despachar", "de": "Versenden", "fr": "Expédier"},
    "Products (select category)": {"it": "Prodotti (selezionare categoria)", "en": "Products (select category)", "es": "Productos (seleccionar categoría)", "de": "Produkte (Kategorie wählen)", "fr": "Produits (sélectionner catégorie)"},
    "-- All --": {"it": "-- Tutte --", "en": "-- All --", "es": "-- Todas --", "de": "-- Alle --", "fr": "-- Tous --"},
    "Product Details": {"it": "Dettagli Prodotto", "en": "Product Details", "es": "Detalles del Producto", "de": "Produktdetails", "fr": "Détails du produit"},
    "Supplier:": {"it": "Fornitore:", "en": "Supplier:", "es": "Proveedor:", "de": "Lieferant:", "fr": "Fournisseur :"},
    "Packaging:": {"it": "Confezionamento:", "en": "Packaging:", "es": "Envase:", "de": "Verpackung:", "fr": "Conditionnement :"},
    "Storage:": {"it": "Conservazione:", "en": "Storage:", "es": "Conservación:", "de": "Lagerung:", "fr": "Stockage :"},
    "In dark:": {"it": "Al buio:", "en": "In dark:", "es": "En oscuridad:", "de": "Im Dunkeln:", "fr": "Dans l'obscurité :"},
    "Category:": {"it": "Categoria:", "en": "Category:", "es": "Categoría:", "de": "Kategorie:", "fr": "Catégorie :"},
    "Stock:": {"it": "Giacenza:", "en": "Stock:", "es": "Existencias:", "de": "Bestand:", "fr": "Stock :"},
    "Select a product!": {"it": "Selezionare un prodotto!", "en": "Select a product!", "es": "¡Seleccione un producto!", "de": "Produkt auswählen!", "fr": "Sélectionnez un produit !"},
    "Select a batch!": {"it": "Selezionare un lotto!", "en": "Select a batch!", "es": "¡Seleccione un lote!", "de": "Charge auswählen!", "fr": "Sélectionnez un lot !"},
    "Unload label": {"it": "Scaricare l'etichetta", "en": "Unload label", "es": "Descargar etiqueta", "de": "Etikett entladen", "fr": "Décharger l'étiquette"},
    "Unload label {}?": {"it": "Scaricare l'etichetta {}?", "en": "Unload label {}?", "es": "¿Descargar etiqueta {}?", "de": "Etikett {} entladen?", "fr": "Décharger l'étiquette {} ?"},
    "Restore label": {"it": "Ripristinare l'etichetta", "en": "Restore label", "es": "Restaurar etiqueta", "de": "Etikett wiederherstellen", "fr": "Restaurer l'étiquette"},
    "Restore label {}?": {"it": "Ripristinare l'etichetta {}?", "en": "Restore label {}?", "es": "¿Restaurar etiqueta {}?", "de": "Etikett {} wiederherstellen?", "fr": "Restaurer l'étiquette {} ?"},
    "Restore cancelled label {}?": {"it": "Ripristinare l'etichetta annullata {}?", "en": "Restore cancelled label {}?", "es": "¿Restaurar etiqueta cancelada {}?", "de": "Storniertes Etikett {} wiederherstellen?", "fr": "Restaurer l'étiquette annulée {} ?"},
    "Cancel label": {"it": "Annullare l'etichetta", "en": "Cancel label", "es": "Cancelar etiqueta", "de": "Etikett stornieren", "fr": "Annuler l'étiquette"},
    "Cancel label {}?": {"it": "Annullare l'etichetta {}?", "en": "Cancel label {}?", "es": "¿Cancelar etiqueta {}?", "de": "Etikett {} stornieren?", "fr": "Annuler l'étiquette {} ?"},
    "Label {} is already cancelled.\nRestore?": {"it": "L'etichetta {} è già annullata.\nRipristinare?", "en": "Label {} is already cancelled.\nRestore?", "es": "La etiqueta {} ya está cancelada.\n¿Restaurar?", "de": "Etikett {} ist bereits storniert.\nWiederherstellen?", "fr": "L'étiquette {} est déjà annulée.\nRestaurer ?"},
    "Label {} has already been unloaded.\nUse 'Unload' to restore.": {"it": "L'etichetta {} è già stata scaricata.\nUsare 'Scarica' per ripristinare.", "en": "Label {} has already been unloaded.\nUse 'Unload' to restore.", "es": "La etiqueta {} ya ha sido descargada.\nUse 'Descargar' para restaurar.", "de": "Etikett {} wurde bereits entladen.\nVerwenden Sie 'Entladen' zum Wiederherstellen.", "fr": "L'étiquette {} a déjà été déchargée.\nUtilisez 'Décharger' pour restaurer."},
    "Label generated and sent to print.": {"it": "Etichetta generata e inviata alla stampa.", "en": "Label generated and sent to print.", "es": "Etiqueta generada y enviada a imprimir.", "de": "Etikett generiert und zum Drucken gesendet.", "fr": "Étiquette générée et envoyée à l'impression."},
    "Error generating label:": {"it": "Errore nella generazione dell'etichetta:", "en": "Error generating label:", "es": "Error al generar la etiqueta:", "de": "Fehler bei der Etikettgenerierung:", "fr": "Erreur lors de la génération de l'étiquette :"},

    # ==========================================================================
    # Products view
    # ==========================================================================
    "New Product": {"it": "Nuovo Prodotto", "en": "New Product", "es": "Nuevo Producto", "de": "Neues Produkt", "fr": "Nouveau produit"},
    "Edit Product": {"it": "Modifica Prodotto", "en": "Edit Product", "es": "Editar Producto", "de": "Produkt bearbeiten", "fr": "Modifier le produit"},
    "Code field is required!": {"it": "Il campo Codice è obbligatorio!", "en": "Code field is required!", "es": "¡El campo Código es obligatorio!", "de": "Code-Feld ist erforderlich!", "fr": "Le champ Code est requis !"},
    "Description field is required!": {"it": "Il campo Descrizione è obbligatorio!", "en": "Description field is required!", "es": "¡El campo Descripción es obligatorio!", "de": "Beschreibung-Feld ist erforderlich!", "fr": "Le champ Description est requis !"},

    # ==========================================================================
    # Packages view
    # ==========================================================================
    "New Package": {"it": "Nuova Confezione", "en": "New Package", "es": "Nuevo Envase", "de": "Neue Packung", "fr": "Nouveau conditionnement"},
    "Edit Package": {"it": "Modifica Confezione", "en": "Edit Package", "es": "Editar Envase", "de": "Packung bearbeiten", "fr": "Modifier le conditionnement"},
    "Supp.Code": {"it": "Cod.Forn.", "en": "Supp.Code", "es": "Cód.Prov.", "de": "Lief.Code", "fr": "Code fourn."},
    "Supplier": {"it": "Fornitore", "en": "Supplier", "es": "Proveedor", "de": "Lieferant", "fr": "Fournisseur"},
    "Lb.": {"it": "Et.", "en": "Lb.", "es": "Etiq.", "de": "Et.", "fr": "Ét."},
    "Packaging": {"it": "Confezionamento", "en": "Packaging", "es": "Envase", "de": "Verpackung", "fr": "Conditionnement"},
    "Storage": {"it": "Conserv.", "en": "Storage", "es": "Conserv.", "de": "Lagerung", "fr": "Stockage"},
    "Source": {"it": "Fonte", "en": "Source", "es": "Fuente", "de": "Quelle", "fr": "Source"},
    "Supplier Code:": {"it": "Cod. Fornitore:", "en": "Supplier Code:", "es": "Código Proveedor:", "de": "Lieferantencode:", "fr": "Code fournisseur :"},
    "Location": {"it": "Ubicazione", "en": "Location", "es": "Ubicación", "de": "Standort", "fr": "Emplacement"},
    "Location:": {"it": "Ubicazione:", "en": "Location:", "es": "Ubicación:", "de": "Standort:", "fr": "Emplacement :"},
    "Source:": {"it": "Fonte:", "en": "Source:", "es": "Fuente:", "de": "Quelle:", "fr": "Source :"},
    "Ordering:": {"it": "Ordinazione:", "en": "Ordering:", "es": "Pedido:", "de": "Bestellung:", "fr": "Commande :"},
    "By piece": {"it": "Al pezzo", "en": "By piece", "es": "Por unidad", "de": "Pro Stück", "fr": "À la pièce"},
    "By package": {"it": "A confezione", "en": "By package", "es": "Por envase", "de": "Pro Packung", "fr": "Par conditionnement"},
    "Pieces per label:": {"it": "Pezzi per etichetta:", "en": "Pieces per label:", "es": "Piezas por etiqueta:", "de": "Stück pro Etikett:", "fr": "Pièces par étiquette :"},
    "Reorder level:": {"it": "Soglia riordino:", "en": "Reorder level:", "es": "Nivel de reorden:", "de": "Nachbestellgrenze:", "fr": "Seuil de réapprovisionnement :"},
    "-- Not assigned --": {"it": "-- Non assegnata --", "en": "-- Not assigned --", "es": "-- Sin asignar --", "de": "-- Nicht zugewiesen --", "fr": "-- Non assigné --"},
    "Select a supplier!": {"it": "Selezionare un fornitore!", "en": "Select a supplier!", "es": "¡Seleccione un proveedor!", "de": "Lieferant auswählen!", "fr": "Sélectionnez un fournisseur !"},
    "Supplier Code field is required!": {"it": "Il campo Codice Fornitore è obbligatorio!", "en": "Supplier Code field is required!", "es": "¡El campo Código Proveedor es obligatorio!", "de": "Lieferantencode-Feld ist erforderlich!", "fr": "Le champ Code fournisseur est requis !"},
    "Packaging field is required!": {"it": "Il campo Confezionamento è obbligatorio!", "en": "Packaging field is required!", "es": "¡El campo Envase es obligatorio!", "de": "Verpackung-Feld ist erforderlich!", "fr": "Le champ Conditionnement est requis !"},
    "Select a storage condition!": {"it": "Selezionare una modalità di conservazione!", "en": "Select a storage condition!", "es": "¡Seleccione una condición de almacenamiento!", "de": "Lagerbedingung auswählen!", "fr": "Sélectionnez une condition de stockage !"},
    "In the dark:": {"it": "Al buio:", "en": "In the dark:", "es": "En oscuridad:", "de": "Im Dunkeln:", "fr": "À l'abri de la lumière :"},
    "Keep in dark": {"it": "Conservare al buio", "en": "Keep in dark", "es": "Conservar en oscuridad", "de": "Dunkel lagern", "fr": "Conserver à l'abri de la lumière"},

    # ==========================================================================
    # Suppliers view
    # ==========================================================================
    "New Supplier": {"it": "Nuovo Fornitore", "en": "New Supplier", "es": "Nuevo Proveedor", "de": "Neuer Lieferant", "fr": "Nouveau fournisseur"},
    "Edit Supplier": {"it": "Modifica Fornitore", "en": "Edit Supplier", "es": "Editar Proveedor", "de": "Lieferant bearbeiten", "fr": "Modifier le fournisseur"},

    # ==========================================================================
    # Categories view
    # ==========================================================================
    "New Category": {"it": "Nuova Categoria", "en": "New Category", "es": "Nueva Categoría", "de": "Neue Kategorie", "fr": "Nouvelle catégorie"},
    "Edit Category": {"it": "Modifica Categoria", "en": "Edit Category", "es": "Editar Categoría", "de": "Kategorie bearbeiten", "fr": "Modifier la catégorie"},

    # ==========================================================================
    # Locations view
    # ==========================================================================
    "New Location": {"it": "Nuova Ubicazione", "en": "New Location", "es": "Nueva Ubicación", "de": "Neuer Standort", "fr": "Nouvel emplacement"},
    "Edit Location": {"it": "Modifica Ubicazione", "en": "Edit Location", "es": "Editar Ubicación", "de": "Standort bearbeiten", "fr": "Modifier l'emplacement"},
    "Room:": {"it": "Stanza:", "en": "Room:", "es": "Sala:", "de": "Raum:", "fr": "Salle :"},

    # ==========================================================================
    # Conservations view
    # ==========================================================================
    "New Storage Condition": {"it": "Nuova Conservazione", "en": "New Storage Condition", "es": "Nueva Condición de Almacenamiento", "de": "Neue Lagerbedingung", "fr": "Nouvelle condition de stockage"},
    "Edit Storage Condition": {"it": "Modifica Conservazione", "en": "Edit Storage Condition", "es": "Editar Condición de Almacenamiento", "de": "Lagerbedingung bearbeiten", "fr": "Modifier la condition de stockage"},

    # ==========================================================================
    # Funding sources view
    # ==========================================================================
    "New Funding Source": {"it": "Nuova Fonte", "en": "New Funding Source", "es": "Nueva Fuente de Financiación", "de": "Neue Finanzierungsquelle", "fr": "Nouvelle source de financement"},
    "Edit Funding Source": {"it": "Modifica Fonte", "en": "Edit Funding Source", "es": "Editar Fuente de Financiación", "de": "Finanzierungsquelle bearbeiten", "fr": "Modifier la source de financement"},

    # ==========================================================================
    # Batch view
    # ==========================================================================
    "Edit Batch": {"it": "Modifica Lotto", "en": "Edit Batch", "es": "Editar Lote", "de": "Charge bearbeiten", "fr": "Modifier le lot"},
    "Batch:": {"it": "Lotto:", "en": "Batch:", "es": "Lote:", "de": "Charge:", "fr": "Lot :"},
    "Expiration:": {"it": "Scadenza:", "en": "Expiration:", "es": "Caducidad:", "de": "Ablauf:", "fr": "Expiration :"},
    "Batch field is required!": {"it": "Il campo Lotto è obbligatorio!", "en": "Batch field is required!", "es": "¡El campo Lote es obligatorio!", "de": "Charge-Feld ist erforderlich!", "fr": "Le champ Lot est requis !"},
    "Expiration field is required!": {"it": "Il campo Scadenza è obbligatorio!", "en": "Expiration field is required!", "es": "¡El campo Caducidad es obligatorio!", "de": "Ablauf-Feld ist erforderlich!", "fr": "Le champ Expiration est requis !"},

    # ==========================================================================
    # Labels view
    # ==========================================================================
    "Load labels": {"it": "Carica etichette", "en": "Load labels", "es": "Cargar etiquetas", "de": "Etiketten laden", "fr": "Charger les étiquettes"},
    "Quantity:": {"it": "Quantità:", "en": "Quantity:", "es": "Cantidad:", "de": "Menge:", "fr": "Quantité :"},
    "Number of labels to create:": {"it": "Numero etichette da creare:", "en": "Number of labels to create:", "es": "Número de etiquetas a crear:", "de": "Anzahl zu erstellender Etiketten:", "fr": "Nombre d'étiquettes à créer :"},
    "Labels created:": {"it": "Etichette create:", "en": "Labels created:", "es": "Etiquetas creadas:", "de": "Etiketten erstellt:", "fr": "Étiquettes créées :"},

    # ==========================================================================
    # Requests view
    # ==========================================================================
    "Reference": {"it": "Riferimento", "en": "Reference", "es": "Referencia", "de": "Referenz", "fr": "Référence"},
    "Date": {"it": "Data", "en": "Date", "es": "Fecha", "de": "Datum", "fr": "Date"},
    "Request Details": {"it": "Dettaglio Richiesta", "en": "Request Details", "es": "Detalles de Solicitud", "de": "Anfragedetails", "fr": "Détails de la demande"},
    "Add Item": {"it": "Aggiungi Articolo", "en": "Add Item", "es": "Agregar Artículo", "de": "Artikel hinzufügen", "fr": "Ajouter un article"},
    "Edit Item": {"it": "Modifica Articolo", "en": "Edit Item", "es": "Editar Artículo", "de": "Artikel bearbeiten", "fr": "Modifier l'article"},
    "Delete Item": {"it": "Elimina Articolo", "en": "Delete Item", "es": "Eliminar Artículo", "de": "Artikel löschen", "fr": "Supprimer l'article"},
    "Close Request": {"it": "Chiudi Richiesta", "en": "Close Request", "es": "Cerrar Solicitud", "de": "Anfrage schließen", "fr": "Fermer la demande"},
    "Delete Request": {"it": "Elimina Richiesta", "en": "Delete Request", "es": "Eliminar Solicitud", "de": "Anfrage löschen", "fr": "Supprimer la demande"},
    "Open": {"it": "Aperte", "en": "Open", "es": "Abiertas", "de": "Offen", "fr": "Ouvertes"},
    "Closed": {"it": "Chiuse", "en": "Closed", "es": "Cerradas", "de": "Geschlossen", "fr": "Fermées"},
    "All": {"it": "Tutte", "en": "All", "es": "Todas", "de": "Alle", "fr": "Tous"},
    "Generate a new request?": {"it": "Generare una nuova richiesta?", "en": "Generate a new request?", "es": "¿Generar una nueva solicitud?", "de": "Neue Anfrage erstellen?", "fr": "Générer une nouvelle demande ?"},
    "New Request": {"it": "Nuova Richiesta", "en": "New Request", "es": "Nueva Solicitud", "de": "Neue Anfrage", "fr": "Nouvelle demande"},
    "Edit Request": {"it": "Modifica Richiesta", "en": "Edit Request", "es": "Editar Solicitud", "de": "Anfrage bearbeiten", "fr": "Modifier la demande"},
    "Reference:": {"it": "Riferimento:", "en": "Reference:", "es": "Referencia:", "de": "Referenz:", "fr": "Référence :"},
    "Date:": {"it": "Data:", "en": "Date:", "es": "Fecha:", "de": "Datum:", "fr": "Date :"},
    "Items": {"it": "Articoli", "en": "Items", "es": "Artículos", "de": "Artikel", "fr": "Articles"},
    "Remove Item": {"it": "Rimuovi Articolo", "en": "Remove Item", "es": "Quitar Artículo", "de": "Artikel entfernen", "fr": "Retirer l'article"},
    "Quantity": {"it": "Quantità", "en": "Quantity", "es": "Cantidad", "de": "Menge", "fr": "Quantité"},
    "Delivered": {"it": "Consegnato", "en": "Delivered", "es": "Entregado", "de": "Geliefert", "fr": "Livré"},
    "Package:": {"it": "Confezione:", "en": "Package:", "es": "Envase:", "de": "Packung:", "fr": "Conditionnement :"},
    "New Item": {"it": "Nuovo Articolo", "en": "New Item", "es": "Nuevo Artículo", "de": "Neuer Artikel", "fr": "Nouvel article"},
    "Ord": {"it": "Ord", "en": "Ord", "es": "Ped", "de": "Best.", "fr": "Com."},
    "Del": {"it": "Eva", "en": "Del", "es": "Ent", "de": "Lief.", "fr": "Livré"},
    "Select a category!": {"it": "Selezionare una categoria!", "en": "Select a category!", "es": "¡Seleccione una categoría!", "de": "Kategorie auswählen!", "fr": "Sélectionnez une catégorie !"},
    "Select a package!": {"it": "Selezionare una confezione!", "en": "Select a package!", "es": "¡Seleccione un envase!", "de": "Packung auswählen!", "fr": "Sélectionnez un conditionnement !"},
    "Quantity must be at least 1!": {"it": "La quantità deve essere almeno 1!", "en": "Quantity must be at least 1!", "es": "¡La cantidad debe ser al menos 1!", "de": "Menge muss mindestens 1 sein!", "fr": "La quantité doit être au moins 1 !"},
    "Item already exists.": {"it": "Articolo già presente.", "en": "Item already exists.", "es": "Artículo ya existe.", "de": "Artikel existiert bereits.", "fr": "L'article existe déjà."},
    "Quantity has been added.": {"it": "La quantità è stata sommata.", "en": "Quantity has been added.", "es": "La cantidad ha sido sumada.", "de": "Menge wurde hinzugefügt.", "fr": "La quantité a été ajoutée."},
    "Drafts": {"it": "Bozze", "en": "Drafts", "es": "Borradores", "de": "Entwürfe", "fr": "Brouillons"},
    "Sent": {"it": "Inviate", "en": "Sent", "es": "Enviadas", "de": "Gesendet", "fr": "Envoyées"},
    "Send Request": {"it": "Invia Richiesta", "en": "Send Request", "es": "Enviar Solicitud", "de": "Anfrage senden", "fr": "Envoyer la demande"},
    "Only drafts can be edited!": {"it": "Solo le bozze possono essere modificate!", "en": "Only drafts can be edited!", "es": "¡Solo los borradores pueden ser editados!", "de": "Nur Entwürfe können bearbeitet werden!", "fr": "Seuls les brouillons peuvent être modifiés !"},
    "Only drafts can be sent!": {"it": "Solo le bozze possono essere inviate!", "en": "Only drafts can be sent!", "es": "¡Solo los borradores pueden ser enviados!", "de": "Nur Entwürfe können gesendet werden!", "fr": "Seuls les brouillons peuvent être envoyés !"},
    "Cannot send a request without items!": {"it": "Impossibile inviare una richiesta senza articoli!", "en": "Cannot send a request without items!", "es": "¡No se puede enviar una solicitud sin artículos!", "de": "Anfrage ohne Artikel kann nicht gesendet werden!", "fr": "Impossible d'envoyer une demande sans articles !"},
    "Send the selected request?": {"it": "Inviare la richiesta selezionata?", "en": "Send the selected request?", "es": "¿Enviar la solicitud seleccionada?", "de": "Ausgewählte Anfrage senden?", "fr": "Envoyer la demande sélectionnée ?"},
    "Items can only be edited in drafts!": {"it": "Articoli modificabili solo nelle bozze!", "en": "Items can only be edited in drafts!", "es": "¡Los artículos solo pueden editarse en borradores!", "de": "Artikel können nur in Entwürfen bearbeitet werden!", "fr": "Les articles ne peuvent être modifiés que dans les brouillons !"},
    "Items can only be deleted in drafts!": {"it": "Articoli eliminabili solo nelle bozze!", "en": "Items can only be deleted in drafts!", "es": "¡Los artículos solo pueden eliminarse en borradores!", "de": "Artikel können nur in Entwürfen gelöscht werden!", "fr": "Les articles ne peuvent être supprimés que dans les brouillons !"},
    "Items can only be cancelled in sent requests!": {"it": "Articoli annullabili solo nelle richieste inviate!", "en": "Items can only be cancelled in sent requests!", "es": "¡Los artículos solo pueden anularse en solicitudes enviadas!", "de": "Artikel können nur in gesendeten Anfragen storniert werden!", "fr": "Les articles ne peuvent être annulés que dans les demandes envoyées !"},
    "Drafts cannot be closed.": {"it": "Le bozze non possono essere chiuse.", "en": "Drafts cannot be closed.", "es": "Los borradores no pueden cerrarse.", "de": "Entwürfe können nicht geschlossen werden.", "fr": "Les brouillons ne peuvent pas être fermés."},
    "Send them first or delete them.": {"it": "Inviarle prima o eliminarle.", "en": "Send them first or delete them.", "es": "Envíelos primero o elimínelos.", "de": "Erst senden oder löschen.", "fr": "Envoyez-les d'abord ou supprimez-les."},
    "The request is already closed!": {"it": "La richiesta è già chiusa!", "en": "The request is already closed!", "es": "¡La solicitud ya está cerrada!", "de": "Die Anfrage ist bereits geschlossen!", "fr": "La demande est déjà fermée !"},
    "Close the selected request?": {"it": "Chiudere la richiesta selezionata?", "en": "Close the selected request?", "es": "¿Cerrar la solicitud seleccionada?", "de": "Ausgewählte Anfrage schließen?", "fr": "Fermer la demande sélectionnée ?"},
    "Cancelled": {"it": "Annullato", "en": "Cancelled", "es": "Anulado", "de": "Storniert", "fr": "Annulé"},
    "Note": {"it": "Nota", "en": "Note", "es": "Nota", "de": "Notiz", "fr": "Note"},
    "There are no more active items.": {"it": "Non ci sono più articoli attivi.", "en": "There are no more active items.", "es": "No hay más artículos activos.", "de": "Keine aktiven Artikel mehr.", "fr": "Il n'y a plus d'articles actifs."},
    "Close the request?": {"it": "Chiudere la richiesta?", "en": "Close the request?", "es": "¿Cerrar la solicitud?", "de": "Anfrage schließen?", "fr": "Fermer la demande ?"},
    "Cancellation reason:": {"it": "Motivo annullamento:", "en": "Cancellation reason:", "es": "Motivo de anulación:", "de": "Stornierungsgrund:", "fr": "Motif d'annulation :"},
    "Cancel Item": {"it": "Annulla Articolo", "en": "Cancel Item", "es": "Anular Artículo", "de": "Artikel stornieren", "fr": "Annuler l'article"},
    "Enter the cancellation reason!": {"it": "Inserire il motivo dell'annullamento!", "en": "Enter the cancellation reason!", "es": "¡Ingrese el motivo de la anulación!", "de": "Stornierungsgrund eingeben!", "fr": "Entrez le motif d'annulation !"},
    "Confirm item cancellation?": {"it": "Confermare l'annullamento dell'articolo?", "en": "Confirm item cancellation?", "es": "¿Confirmar anulación del artículo?", "de": "Artikelstornierung bestätigen?", "fr": "Confirmer l'annulation de l'article ?"},
    "The item has already been cancelled.": {"it": "L'articolo è già stato annullato.", "en": "The item has already been cancelled.", "es": "El artículo ya ha sido anulado.", "de": "Der Artikel wurde bereits storniert.", "fr": "L'article a déjà été annulé."},
    "Cannot delete a cancelled item.": {"it": "Impossibile eliminare un articolo annullato.", "en": "Cannot delete a cancelled item.", "es": "No se puede eliminar un artículo anulado.", "de": "Stornierter Artikel kann nicht gelöscht werden.", "fr": "Impossible de supprimer un article annulé."},
    "Item cancelled.": {"it": "Articolo annullato.", "en": "Item cancelled.", "es": "Artículo anulado.", "de": "Artikel storniert.", "fr": "Article annulé."},
    "Reason": {"it": "Motivo", "en": "Reason", "es": "Motivo", "de": "Grund", "fr": "Motif"},
    "Detail:": {"it": "Dettaglio:", "en": "Detail:", "es": "Detalle:", "de": "Detail:", "fr": "Détail :"},
    "Note:": {"it": "Nota:", "en": "Note:", "es": "Nota:", "de": "Notiz:", "fr": "Note :"},
    "Delete the selected item?": {"it": "Eliminare l'articolo selezionato?", "en": "Delete the selected item?", "es": "¿Eliminar el artículo seleccionado?", "de": "Ausgewählten Artikel löschen?", "fr": "Supprimer l'article sélectionné ?"},
    "Eliminare la richiesta '{}' e tutti i suoi articoli?": {"it": "Eliminare la richiesta '{}' e tutti i suoi articoli?", "en": "Delete request '{}' and all its items?", "es": "¿Eliminar la solicitud '{}' y todos sus artículos?", "de": "Anfrage '{}' und alle Artikel löschen?", "fr": "Supprimer la demande '{}' et tous ses articles ?"},
    "The request contains no items.": {"it": "La richiesta non contiene articoli.", "en": "The request contains no items.", "es": "La solicitud no contiene artículos.", "de": "Die Anfrage enthält keine Artikel.", "fr": "La demande ne contient aucun article."},
    "Error generating report:": {"it": "Errore nella generazione del report:", "en": "Error generating report:", "es": "Error al generar el informe:", "de": "Fehler bei der Berichtserstellung:", "fr": "Erreur lors de la génération du rapport :"},
    "Select a request first!": {"it": "Selezionare prima una richiesta!", "en": "Select a request first!", "es": "¡Seleccione primero una solicitud!", "de": "Zuerst eine Anfrage auswählen!", "fr": "Sélectionnez d'abord une demande !"},
    "Select an item!": {"it": "Selezionare un articolo!", "en": "Select an item!", "es": "¡Seleccione un artículo!", "de": "Artikel auswählen!", "fr": "Sélectionnez un élément !"},
    "Printing disabled on this workstation.": {"it": "Stampa disabilitata su questa postazione.", "en": "Printing disabled on this workstation.", "es": "Impresión deshabilitada en esta estación.", "de": "Drucken auf dieser Arbeitsstation deaktiviert.", "fr": "Impression désactivée sur ce poste."},
    "Local settings": {"it": "Impostazioni locali", "en": "Local settings", "es": "Configuración local", "de": "Lokale Einstellungen", "fr": "Paramètres locaux"},
    "Label printing:": {"it": "Stampa etichette:", "en": "Label printing:", "es": "Impresión de etiquetas:", "de": "Etikettendruck:", "fr": "Impression d'étiquettes :"},
    "Enabled on this workstation": {"it": "Abilitata su questa postazione", "en": "Enabled on this workstation", "es": "Habilitada en esta estación", "de": "Auf dieser Arbeitsstation aktiviert", "fr": "Activée sur ce poste"},

    # ==========================================================================
    # Delivery view
    # ==========================================================================
    "New Delivery": {"it": "Nuova Consegna", "en": "New Delivery", "es": "Nueva Entrega", "de": "Neue Lieferung", "fr": "Nouvelle livraison"},
    "Record Delivery": {"it": "Registra Consegna", "en": "Record Delivery", "es": "Registrar Entrega", "de": "Lieferung erfassen", "fr": "Enregistrer la livraison"},
    "Delivery date:": {"it": "Data consegna:", "en": "Delivery date:", "es": "Fecha de entrega:", "de": "Lieferdatum:", "fr": "Date de livraison :"},
    "Quantity delivered:": {"it": "Quantità consegnata:", "en": "Quantity delivered:", "es": "Cantidad entregada:", "de": "Gelieferte Menge:", "fr": "Quantité livrée :"},
    "Open requests": {"it": "Richieste aperte", "en": "Open requests", "es": "Solicitudes abiertas", "de": "Offene Anfragen", "fr": "Demandes ouvertes"},
    "Open Requests": {"it": "Richieste Aperte", "en": "Open Requests", "es": "Solicitudes Abiertas", "de": "Offene Anfragen", "fr": "Demandes ouvertes"},
    "Select request": {"it": "Seleziona richiesta", "en": "Select request", "es": "Seleccionar solicitud", "de": "Anfrage auswählen", "fr": "Sélectionner la demande"},
    "Items to Fulfill": {"it": "Articoli da Evadere", "en": "Items to Fulfill", "es": "Artículos a Despachar", "de": "Zu erfüllende Artikel", "fr": "Articles à traiter"},
    "Item Details": {"it": "Dettaglio Articolo", "en": "Item Details", "es": "Detalle del Artículo", "de": "Artikeldetails", "fr": "Détails de l'article"},
    "Already Fulfilled:": {"it": "Già Evaso:", "en": "Already Fulfilled:", "es": "Ya Despachado:", "de": "Bereits erfüllt:", "fr": "Déjà traité :"},
    "Delivery Note:": {"it": "DDT:", "en": "Delivery Note:", "es": "Albarán:", "de": "Lieferschein:", "fr": "Bon de livraison :"},
    "Delivery Date:": {"it": "Data Consegna:", "en": "Delivery Date:", "es": "Fecha de Entrega:", "de": "Lieferdatum:", "fr": "Date de livraison :"},
    "Select existing:": {"it": "Seleziona esistente:", "en": "Select existing:", "es": "Seleccionar existente:", "de": "Vorhandene auswählen:", "fr": "Sélectionner existant :"},
    "Create new:": {"it": "Crea nuovo:", "en": "Create new:", "es": "Crear nuevo:", "de": "Neu erstellen:", "fr": "Créer nouveau :"},
    "Exp": {"it": "Scad", "en": "Exp", "es": "Cad", "de": "Abl.", "fr": "Exp"},
    "Select an item to fulfill!": {"it": "Selezionare un articolo da evadere!", "en": "Select an item to fulfill!", "es": "¡Seleccione un artículo a despachar!", "de": "Artikel zur Erfüllung auswählen!", "fr": "Sélectionnez un article à traiter !"},
    "Enter the delivery note number!": {"it": "Inserire il numero DDT!", "en": "Enter the delivery note number!", "es": "¡Ingrese el número del albarán!", "de": "Lieferscheinnummer eingeben!", "fr": "Entrez le numéro du bon de livraison !"},
    "Invalid delivery date!": {"it": "Data consegna non valida!", "en": "Invalid delivery date!", "es": "¡Fecha de entrega no válida!", "de": "Ungültiges Lieferdatum!", "fr": "Date de livraison invalide !"},
    "Quantity must be between 1 and": {"it": "La quantità deve essere tra 1 e", "en": "Quantity must be between 1 and", "es": "La cantidad debe estar entre 1 y", "de": "Menge muss zwischen 1 und", "fr": "La quantité doit être entre 1 et"},
    "Quantity must be a multiple of": {"it": "La quantità deve essere un multiplo di", "en": "Quantity must be a multiple of", "es": "La cantidad debe ser múltiplo de", "de": "Menge muss ein Vielfaches von", "fr": "La quantité doit être un multiple de"},
    "Select an existing batch!": {"it": "Selezionare un lotto esistente!", "en": "Select an existing batch!", "es": "¡Seleccione un lote existente!", "de": "Vorhandene Charge auswählen!", "fr": "Sélectionnez un lot existant !"},
    "Enter the batch number!": {"it": "Inserire il numero di lotto!", "en": "Enter the batch number!", "es": "¡Ingrese el número de lote!", "de": "Chargennummer eingeben!", "fr": "Entrez le numéro de lot !"},
    "Invalid expiration date!": {"it": "Data scadenza non valida!", "en": "Invalid expiration date!", "es": "¡Fecha de caducidad no válida!", "de": "Ungültiges Ablaufdatum!", "fr": "Date d'expiration invalide !"},
    "Expiration date must be in the future!": {"it": "La data di scadenza deve essere futura!", "en": "Expiration date must be in the future!", "es": "¡La fecha de caducidad debe ser futura!", "de": "Ablaufdatum muss in der Zukunft liegen!", "fr": "La date d'expiration doit être dans le futur !"},
    "Batch": {"it": "Il lotto", "en": "Batch", "es": "El lote", "de": "Charge", "fr": "Lot"},
    "with expiration": {"it": "con scadenza", "en": "with expiration", "es": "con caducidad", "de": "mit Ablauf", "fr": "avec expiration"},
    "Select it from the existing batches list.": {"it": "Selezionarlo dalla lista dei lotti esistenti.", "en": "Select it from the existing batches list.", "es": "Selecciónelo de la lista de lotes existentes.", "de": "Aus der Liste der vorhandenen Chargen auswählen.", "fr": "Sélectionnez-le dans la liste des lots existants."},
    "Record delivery of": {"it": "Registrare la consegna di", "en": "Record delivery of", "es": "Registrar entrega de", "de": "Lieferung erfassen von", "fr": "Enregistrer la livraison de"},
    "units?": {"it": "unità?", "en": "units?", "es": "unidades?", "de": "Einheiten?", "fr": "unités ?"},
    "Will create": {"it": "Verranno create", "en": "Will create", "es": "Se crearán", "de": "Wird erstellen", "fr": "Va créer"},
    "labels.": {"it": "etichette.", "en": "labels.", "es": "etiquetas.", "de": "Etiketten.", "fr": "étiquettes."},
    "label": {"it": "etichetta", "en": "label", "es": "etiqueta", "de": "Etikett", "fr": "étiquette"},
    "Error creating batch!": {"it": "Errore nella creazione del lotto!", "en": "Error creating batch!", "es": "¡Error al crear el lote!", "de": "Fehler beim Erstellen der Charge!", "fr": "Erreur lors de la création du lot !"},
    "Error recording delivery!": {"it": "Errore nella registrazione della consegna!", "en": "Error recording delivery!", "es": "¡Error al registrar la entrega!", "de": "Fehler beim Erfassen der Lieferung!", "fr": "Erreur lors de l'enregistrement de la livraison !"},
    "Delivery recorded successfully!": {"it": "Consegna registrata con successo!", "en": "Delivery recorded successfully!", "es": "¡Entrega registrada con éxito!", "de": "Lieferung erfolgreich erfasst!", "fr": "Livraison enregistrée avec succès !"},
    "Created": {"it": "Create", "en": "Created", "es": "Creadas", "de": "Erstellt", "fr": "Créées"},
    "Error during save:": {"it": "Errore durante il salvataggio:", "en": "Error during save:", "es": "Error al guardar:", "de": "Fehler beim Speichern:", "fr": "Erreur lors de l'enregistrement :"},
    "All items have been fulfilled.": {"it": "Tutti gli articoli sono stati evasi.", "en": "All items have been fulfilled.", "es": "Todos los artículos han sido despachados.", "de": "Alle Artikel wurden erfüllt.", "fr": "Tous les articles ont été traités."},
    "The request has been closed.": {"it": "La richiesta è stata chiusa.", "en": "The request has been closed.", "es": "La solicitud ha sido cerrada.", "de": "Die Anfrage wurde geschlossen.", "fr": "La demande a été fermée."},

    # ==========================================================================
    # Stocks view
    # ==========================================================================
    "Print Type": {"it": "Tipo Stampa", "en": "Print Type", "es": "Tipo de Impresión", "de": "Drucktyp", "fr": "Type d'impression"},
    "Print stock": {"it": "Stampa giacenze", "en": "Print stock", "es": "Imprimir existencias", "de": "Bestand drucken", "fr": "Imprimer le stock"},
    "Export": {"it": "Esporta", "en": "Export", "es": "Exportar", "de": "Exportieren", "fr": "Exporter"},

    # ==========================================================================
    # Expiring view
    # ==========================================================================
    "Expired Batches": {"it": "Lotti Scaduti", "en": "Expired Batches", "es": "Lotes Caducados", "de": "Abgelaufene Chargen", "fr": "Lots expirés"},
    "Upcoming expirations": {"it": "Scadenze prossime", "en": "Upcoming expirations", "es": "Próximas caducidades", "de": "Bevorstehende Abläufe", "fr": "Expirations à venir"},
    "Days:": {"it": "Giorni:", "en": "Days:", "es": "Días:", "de": "Tage:", "fr": "Jours :"},
    "Days to expiration": {"it": "Giorni alla scadenza", "en": "Days to expiration", "es": "Días hasta caducidad", "de": "Tage bis Ablauf", "fr": "Jours avant expiration"},

    # ==========================================================================
    # Barcode view
    # ==========================================================================
    "Unload labels": {"it": "Scarico etichette", "en": "Unload labels", "es": "Descarga de etiquetas", "de": "Etiketten entladen", "fr": "Décharger les étiquettes"},
    "Unload Label": {"it": "Scarico Etichetta", "en": "Unload Label", "es": "Descargar Etiqueta", "de": "Etikett entladen", "fr": "Décharger l'étiquette"},
    "Scan barcode or enter label code:": {"it": "Scansiona il barcode o inserisci il codice etichetta:", "en": "Scan barcode or enter label code:", "es": "Escanear código de barras o ingresar código de etiqueta:", "de": "Barcode scannen oder Etikettencode eingeben:", "fr": "Scanner le code-barres ou entrer le code étiquette :"},
    "Barcode:": {"it": "Codice a barre:", "en": "Barcode:", "es": "Código de barras:", "de": "Barcode:", "fr": "Code-barres :"},
    "Invalid code!": {"it": "Codice non valido!", "en": "Invalid code!", "es": "¡Código inválido!", "de": "Ungültiger Code!", "fr": "Code invalide !"},
    "Label": {"it": "Etichetta", "en": "Label", "es": "Etiqueta", "de": "Etikett", "fr": "Étiquette"},
    "not found!": {"it": "non trovata!", "en": "not found!", "es": "¡no encontrada!", "de": "nicht gefunden!", "fr": "non trouvée !"},
    "already unloaded!": {"it": "già scaricata!", "en": "already unloaded!", "es": "¡ya descargada!", "de": "bereits entladen!", "fr": "déjà déchargée !"},
    "cancelled!": {"it": "annullata!", "en": "cancelled!", "es": "¡cancelada!", "de": "storniert!", "fr": "annulée !"},
    "Unloaded:": {"it": "Scaricata:", "en": "Unloaded:", "es": "Descargada:", "de": "Entladen:", "fr": "Déchargée :"},
    "Error unloading!": {"it": "Errore nello scarico!", "en": "Error unloading!", "es": "¡Error al descargar!", "de": "Fehler beim Entladen!", "fr": "Erreur lors du déchargement !"},
    "Label unloaded:": {"it": "Etichetta scaricata:", "en": "Label unloaded:", "es": "Etiqueta descargada:", "de": "Etikett entladen:", "fr": "Étiquette déchargée :"},
    "Label not found!": {"it": "Etichetta non trovata!", "en": "Label not found!", "es": "¡Etiqueta no encontrada!", "de": "Etikett nicht gefunden!", "fr": "Étiquette non trouvée !"},
    "Label already unloaded!": {"it": "Etichetta già scaricata!", "en": "Label already unloaded!", "es": "¡Etiqueta ya descargada!", "de": "Etikett bereits entladen!", "fr": "Étiquette déjà déchargée !"},

    # ==========================================================================
    # Custom label view
    # ==========================================================================
    "Lines to print": {"it": "Righe da stampare", "en": "Lines to print", "es": "Líneas a imprimir", "de": "Zu druckende Zeilen", "fr": "Lignes à imprimer"},
    "Label Text": {"it": "Testo Etichetta", "en": "Label Text", "es": "Texto de Etiqueta", "de": "Etikettentext", "fr": "Texte de l'étiquette"},
    "Include laboratory name": {"it": "Includi nome laboratorio", "en": "Include laboratory name", "es": "Incluir nombre del laboratorio", "de": "Laborname einschließen", "fr": "Inclure le nom du laboratoire"},
    "Saved Templates": {"it": "Modelli Salvati", "en": "Saved Templates", "es": "Plantillas Guardadas", "de": "Gespeicherte Vorlagen", "fr": "Modèles enregistrés"},
    "Custom label": {"it": "Etichetta personalizzata", "en": "Custom label", "es": "Etiqueta personalizada", "de": "Benutzerdefiniertes Etikett", "fr": "Étiquette personnalisée"},
    "Text line 1:": {"it": "Testo riga 1:", "en": "Text line 1:", "es": "Texto línea 1:", "de": "Textzeile 1:", "fr": "Ligne de texte 1 :"},
    "Text line 2:": {"it": "Testo riga 2:", "en": "Text line 2:", "es": "Texto línea 2:", "de": "Textzeile 2:", "fr": "Ligne de texte 2 :"},
    "Text line 3:": {"it": "Testo riga 3:", "en": "Text line 3:", "es": "Texto línea 3:", "de": "Textzeile 3:", "fr": "Ligne de texte 3 :"},
    "Barcode code:": {"it": "Codice barcode:", "en": "Barcode code:", "es": "Código de barras:", "de": "Barcode-Code:", "fr": "Code code-barres :"},

    # ==========================================================================
    # Statistics views
    # ==========================================================================
    "Analysis Period": {"it": "Periodo di Analisi", "en": "Analysis Period", "es": "Período de Análisis", "de": "Analysezeitraum", "fr": "Période d'analyse"},
    "Summary": {"it": "Riepilogo", "en": "Summary", "es": "Resumen", "de": "Zusammenfassung", "fr": "Résumé"},
    "Expiration Analysis": {"it": "Analisi Scadenze", "en": "Expiration Analysis", "es": "Análisis de Caducidades", "de": "Ablaufanalyse", "fr": "Analyse des expirations"},
    "Historical Expired Analysis": {"it": "Analisi Storica Scaduti", "en": "Historical Expired Analysis", "es": "Análisis Histórico de Caducados", "de": "Historische Ablaufanalyse", "fr": "Analyse historique des expirations"},
    "Expiration period - From:": {"it": "Periodo scadenza - Da:", "en": "Expiration period - From:", "es": "Período de caducidad - Desde:", "de": "Ablaufzeitraum - Von:", "fr": "Période d'expiration - De :"},
    "Last year": {"it": "Anno scorso", "en": "Last year", "es": "Año pasado", "de": "Letztes Jahr", "fr": "Année dernière"},
    "6 months ago": {"it": "6 mesi fa", "en": "6 months ago", "es": "Hace 6 meses", "de": "Vor 6 Monaten", "fr": "Il y a 6 mois"},
    "Today": {"it": "Oggi", "en": "Today", "es": "Hoy", "de": "Heute", "fr": "Aujourd'hui"},
    "+30 days": {"it": "+30 gg", "en": "+30 days", "es": "+30 días", "de": "+30 Tage", "fr": "+30 jours"},
    "+90 days": {"it": "+90 gg", "en": "+90 days", "es": "+90 días", "de": "+90 Tage", "fr": "+90 jours"},
    "30 days": {"it": "30 gg", "en": "30 days", "es": "30 días", "de": "30 Tage", "fr": "30 jours"},
    "90 days": {"it": "90 gg", "en": "90 days", "es": "90 días", "de": "90 Tage", "fr": "90 jours"},
    "6 months": {"it": "6 mesi", "en": "6 months", "es": "6 meses", "de": "6 Monate", "fr": "6 mois"},
    "Year": {"it": "Anno", "en": "Year", "es": "Año", "de": "Jahr", "fr": "Année"},
    "Expired Batches (with remaining stock)": {"it": "Lotti Scaduti (con giacenza residua)", "en": "Expired Batches (with remaining stock)", "es": "Lotes Caducados (con existencias restantes)", "de": "Abgelaufene Chargen (mit Restbestand)", "fr": "Lots expirés (avec stock restant)"},
    "FEFO Efficiency (First Expired First Out)": {"it": "Efficienza FEFO (First Expired First Out)", "en": "FEFO Efficiency (First Expired First Out)", "es": "Eficiencia FEFO (Primero en Caducar, Primero en Salir)", "de": "FEFO-Effizienz (First Expired First Out)", "fr": "Efficacité FEFO (Premier expiré, premier sorti)"},
    "Remaining": {"it": "Residuo", "en": "Remaining", "es": "Restante", "de": "Verbleibend", "fr": "Restant"},
    "Used": {"it": "Usato", "en": "Used", "es": "Usado", "de": "Verwendet", "fr": "Utilisé"},
    "Loss %": {"it": "Perdita %", "en": "Loss %", "es": "Pérdida %", "de": "Verlust %", "fr": "Perte %"},
    "Unloaded Labels": {"it": "Etichette Scaricate", "en": "Unloaded Labels", "es": "Etiquetas Descargadas", "de": "Entladene Etiketten", "fr": "Étiquettes déchargées"},
    "FEFO Correct": {"it": "FEFO Corrette", "en": "FEFO Correct", "es": "FEFO Correctas", "de": "FEFO korrekt", "fr": "FEFO Correct"},
    "Efficiency %": {"it": "Efficienza %", "en": "Efficiency %", "es": "Eficiencia %", "de": "Effizienz %", "fr": "Efficacité %"},
    "Expired batches with stock:": {"it": "Lotti scaduti con giacenza:", "en": "Expired batches with stock:", "es": "Lotes caducados con existencias:", "de": "Abgelaufene Chargen mit Bestand:", "fr": "Lots expirés avec stock :"},
    "Expired labels (losses):": {"it": "Etichette scadute (perdite):", "en": "Expired labels (losses):", "es": "Etiquetas caducadas (pérdidas):", "de": "Abgelaufene Etiketten (Verluste):", "fr": "Étiquettes expirées (pertes) :"},
    "Expiring (30 days):": {"it": "In scadenza (30 gg):", "en": "Expiring (30 days):", "es": "Por caducar (30 días):", "de": "Ablaufend (30 Tage):", "fr": "Expirant (30 jours) :"},
    "Supplier Analysis": {"it": "Analisi Fornitori", "en": "Supplier Analysis", "es": "Análisis de Proveedores", "de": "Lieferantenanalyse", "fr": "Analyse fournisseurs"},
    "Orders": {"it": "Ordini", "en": "Orders", "es": "Pedidos", "de": "Bestellungen", "fr": "Commandes"},
    "Ordered": {"it": "Ordinato", "en": "Ordered", "es": "Pedido", "de": "Bestellt", "fr": "Commandé"},
    "Completion %": {"it": "Completamento %", "en": "Completion %", "es": "Completado %", "de": "Fertigstellung %", "fr": "Achèvement %"},
    "Avg TAT (days)": {"it": "TAT medio (gg)", "en": "Avg TAT (days)", "es": "TAT promedio (días)", "de": "Durchschn. TAT (Tage)", "fr": "TAT moyen (jours)"},
    "Time Analysis (TAT)": {"it": "Analisi Tempi (TAT)", "en": "Time Analysis (TAT)", "es": "Análisis de Tiempos (TAT)", "de": "Zeitanalyse (TAT)", "fr": "Analyse des délais (TAT)"},
    "TAT Metrics": {"it": "Metriche TAT", "en": "TAT Metrics", "es": "Métricas TAT", "de": "TAT-Metriken", "fr": "Métriques TAT"},
    "Request → Delivery Time (by supplier)": {"it": "Tempo Richiesta → Consegna (per fornitore)", "en": "Request → Delivery Time (by supplier)", "es": "Tiempo Solicitud → Entrega (por proveedor)", "de": "Anfrage → Lieferzeit (nach Lieferant)", "fr": "Délai Demande → Livraison (par fournisseur)"},
    "Warehouse Time (Load → Unload)": {"it": "Tempo in Magazzino (Carico → Scarico)", "en": "Warehouse Time (Load → Unload)", "es": "Tiempo en Almacén (Carga → Descarga)", "de": "Lagerzeit (Laden → Entladen)", "fr": "Temps en entrepôt (Chargement → Déchargement)"},
    "Avg (days)": {"it": "Media (gg)", "en": "Avg (days)", "es": "Promedio (días)", "de": "Durchschn. (Tage)", "fr": "Moy. (jours)"},
    "Min (days)": {"it": "Min (gg)", "en": "Min (days)", "es": "Mín (días)", "de": "Min (Tage)", "fr": "Min (jours)"},
    "Max (days)": {"it": "Max (gg)", "en": "Max (days)", "es": "Máx (días)", "de": "Max (Tage)", "fr": "Max (jours)"},
    "Avg order TAT:": {"it": "TAT medio ordini:", "en": "Avg order TAT:", "es": "TAT promedio pedidos:", "de": "Durchschn. Bestell-TAT:", "fr": "TAT moyen commandes :"},
    "Avg warehouse TAT:": {"it": "TAT medio magazzino:", "en": "Avg warehouse TAT:", "es": "TAT promedio almacén:", "de": "Durchschn. Lager-TAT:", "fr": "TAT moyen entrepôt :"},
    "days": {"it": "giorni", "en": "days", "es": "días", "de": "Tage", "fr": "jours"},
    "Consumption Analysis": {"it": "Analisi Consumi", "en": "Consumption Analysis", "es": "Análisis de Consumos", "de": "Verbrauchsanalyse", "fr": "Analyse de la consommation"},
    "Consumption by Product": {"it": "Consumi per Prodotto", "en": "Consumption by Product", "es": "Consumos por Producto", "de": "Verbrauch nach Produkt", "fr": "Consommation par produit"},
    "Consumption by Category": {"it": "Consumi per Categoria", "en": "Consumption by Category", "es": "Consumos por Categoría", "de": "Verbrauch nach Kategorie", "fr": "Consommation par catégorie"},
    "Rotation Analysis": {"it": "Analisi Rotazione", "en": "Rotation Analysis", "es": "Análisis de Rotación", "de": "Rotationsanalyse", "fr": "Analyse de rotation"},
    "Rotation and ABC Analysis": {"it": "Analisi Rotazione e ABC", "en": "Rotation and ABC Analysis", "es": "Análisis de Rotación y ABC", "de": "Rotations- und ABC-Analyse", "fr": "Analyse rotation et ABC"},
    "Statistics Dashboard": {"it": "Dashboard Statistiche", "en": "Statistics Dashboard", "es": "Panel de Estadísticas", "de": "Statistik-Dashboard", "fr": "Tableau de bord statistiques"},
    "Warehouse Dashboard": {"it": "Dashboard Magazzino", "en": "Warehouse Dashboard", "es": "Panel de Almacén", "de": "Lager-Dashboard", "fr": "Tableau de bord entrepôt"},
    "Below Reorder Threshold": {"it": "Sotto Soglia Riordino", "en": "Below Reorder Threshold", "es": "Bajo Umbral de Reorden", "de": "Unter Nachbestellgrenze", "fr": "Sous le seuil de réapprovisionnement"},
    "Movements (last 30 days)": {"it": "Movimenti (ultimi 30 giorni)", "en": "Movements (last 30 days)", "es": "Movimientos (últimos 30 días)", "de": "Bewegungen (letzte 30 Tage)", "fr": "Mouvements (30 derniers jours)"},
    "Top 5 Consumption (30 days)": {"it": "Top 5 Consumi (30 giorni)", "en": "Top 5 Consumption (30 days)", "es": "Top 5 Consumos (30 días)", "de": "Top 5 Verbrauch (30 Tage)", "fr": "Top 5 consommation (30 jours)"},
    "Active products:": {"it": "Prodotti attivi:", "en": "Active products:", "es": "Productos activos:", "de": "Aktive Produkte:", "fr": "Produits actifs :"},
    "Labels in stock:": {"it": "Etichette in giacenza:", "en": "Labels in stock:", "es": "Etiquetas en existencia:", "de": "Etiketten im Bestand:", "fr": "Étiquettes en stock :"},
    "Active batches:": {"it": "Lotti attivi:", "en": "Active batches:", "es": "Lotes activos:", "de": "Aktive Chargen:", "fr": "Lots actifs :"},
    "Products below threshold:": {"it": "Prodotti sotto soglia:", "en": "Products below threshold:", "es": "Productos bajo umbral:", "de": "Produkte unter Grenze:", "fr": "Produits sous le seuil :"},
    "Out of stock products:": {"it": "Prodotti esauriti:", "en": "Out of stock products:", "es": "Productos agotados:", "de": "Nicht vorrätige Produkte:", "fr": "Produits en rupture :"},
    "Expired batches:": {"it": "Lotti scaduti:", "en": "Expired batches:", "es": "Lotes caducados:", "de": "Abgelaufene Chargen:", "fr": "Lots expirés :"},
    "Expiring (60 days):": {"it": "In scadenza (60 gg):", "en": "Expiring (60 days):", "es": "Por caducar (60 días):", "de": "Ablaufend (60 Tage):", "fr": "Expirant (60 jours) :"},
    "Expiring (90 days):": {"it": "In scadenza (90 gg):", "en": "Expiring (90 days):", "es": "Por caducar (90 días):", "de": "Ablaufend (90 Tage):", "fr": "Expirant (90 jours) :"},
    "Labels loaded:": {"it": "Etichette caricate:", "en": "Labels loaded:", "es": "Etiquetas cargadas:", "de": "Etiketten geladen:", "fr": "Étiquettes chargées :"},
    "Labels unloaded:": {"it": "Etichette scaricate:", "en": "Labels unloaded:", "es": "Etiquetas descargadas:", "de": "Etiketten entladen:", "fr": "Étiquettes déchargées :"},
    "Labels cancelled:": {"it": "Etichette annullate:", "en": "Labels cancelled:", "es": "Etiquetas canceladas:", "de": "Etiketten storniert:", "fr": "Étiquettes annulées :"},
    "Open requests:": {"it": "Richieste aperte:", "en": "Open requests:", "es": "Solicitudes abiertas:", "de": "Offene Anfragen:", "fr": "Demandes ouvertes :"},
    "Pending items:": {"it": "Articoli in attesa:", "en": "Pending items:", "es": "Artículos pendientes:", "de": "Ausstehende Artikel:", "fr": "Articles en attente :"},
    "No data available": {"it": "Nessun dato disponibile", "en": "No data available", "es": "Sin datos disponibles", "de": "Keine Daten verfügbar", "fr": "Aucune donnée disponible"},
    "Stock": {"it": "Giacenza", "en": "Stock", "es": "Existencias", "de": "Bestand", "fr": "Stock"},
    "Consumed": {"it": "Consumato", "en": "Consumed", "es": "Consumido", "de": "Verbraucht", "fr": "Consommé"},
    "Filters": {"it": "Filtri", "en": "Filters", "es": "Filtros", "de": "Filter", "fr": "Filtres"},
    "Avg/Month": {"it": "Media/Mese", "en": "Avg/Month", "es": "Prom/Mes", "de": "Durchschn./Monat", "fr": "Moy./Mois"},
    "Total products": {"it": "Totale prodotti", "en": "Total products", "es": "Total productos", "de": "Produkte gesamt", "fr": "Total produits"},
    "Total consumed": {"it": "Totale consumato", "en": "Total consumed", "es": "Total consumido", "de": "Gesamt verbraucht", "fr": "Total consommé"},
    "Period": {"it": "Periodo", "en": "Period", "es": "Período", "de": "Zeitraum", "fr": "Période"},
    "Export Consumption": {"it": "Esporta Consumi", "en": "Export Consumption", "es": "Exportar Consumos", "de": "Verbrauch exportieren", "fr": "Exporter consommation"},
    "60 days": {"it": "60 gg", "en": "60 days", "es": "60 días", "de": "60 Tage", "fr": "60 jours"},
    "ABC Classification": {"it": "Classificazione ABC", "en": "ABC Classification", "es": "Clasificación ABC", "de": "ABC-Klassifizierung", "fr": "Classification ABC"},
    "ABC Classification:": {"it": "Classificazione ABC:", "en": "ABC Classification:", "es": "Clasificación ABC:", "de": "ABC-Klassifizierung:", "fr": "Classification ABC :"},
    "A = High rotation (80% movements)": {"it": "A = Alta rotazione (80% movimenti)", "en": "A = High rotation (80% movements)", "es": "A = Alta rotación (80% movimientos)", "de": "A = Hohe Rotation (80% Bewegungen)", "fr": "A = Haute rotation (80% mouvements)"},
    "B = Medium rotation": {"it": "B = Media rotazione", "en": "B = Medium rotation", "es": "B = Media rotación", "de": "B = Mittlere Rotation", "fr": "B = Rotation moyenne"},
    "C = Low rotation": {"it": "C = Bassa rotazione", "en": "C = Low rotation", "es": "C = Baja rotación", "de": "C = Niedrige Rotation", "fr": "C = Rotation faible"},
    "Coverage (days)": {"it": "Copertura (gg)", "en": "Coverage (days)", "es": "Cobertura (días)", "de": "Reichweite (Tage)", "fr": "Couverture (jours)"},
    "ABC": {"it": "ABC", "en": "ABC", "es": "ABC", "de": "ABC", "fr": "ABC"},
    "Class A": {"it": "Classe A", "en": "Class A", "es": "Clase A", "de": "Klasse A", "fr": "Classe A"},
    "Class B": {"it": "Classe B", "en": "Class B", "es": "Clase B", "de": "Klasse B", "fr": "Classe B"},
    "Class C": {"it": "Classe C", "en": "Class C", "es": "Clase C", "de": "Klasse C", "fr": "Classe C"},
    "Export Rotation": {"it": "Esporta Rotazione", "en": "Export Rotation", "es": "Exportar Rotación", "de": "Rotation exportieren", "fr": "Exporter rotation"},
    "Class": {"it": "Classe", "en": "Class", "es": "Clase", "de": "Klasse", "fr": "Classe"},
    "Cumulative %": {"it": "% Cumulativa", "en": "Cumulative %", "es": "% Acumulado", "de": "Kumulativ %", "fr": "% Cumulé"},

    # ==========================================================================
    # Package history view
    # ==========================================================================
    "Order History": {"it": "Storico Ordini", "en": "Order History", "es": "Historial de Pedidos", "de": "Bestellverlauf", "fr": "Historique des commandes"},
    "Request": {"it": "Richiesta", "en": "Request", "es": "Solicitud", "de": "Anfrage", "fr": "Demande"},
    "Request Date": {"it": "Data Richiesta", "en": "Request Date", "es": "Fecha de Solicitud", "de": "Anfragedatum", "fr": "Date de demande"},
    "Qty Ordered": {"it": "Qty Ordinata", "en": "Qty Ordered", "es": "Cant. Pedida", "de": "Bestellmenge", "fr": "Qté commandée"},
    "Qty Delivered": {"it": "Qty Consegnata", "en": "Qty Delivered", "es": "Cant. Entregada", "de": "Liefermenge", "fr": "Qté livrée"},
    "Delivery Date": {"it": "Data Consegna", "en": "Delivery Date", "es": "Fecha de Entrega", "de": "Lieferdatum", "fr": "Date de livraison"},

    # ==========================================================================
    # Messages
    # ==========================================================================
    "Do you want to save?": {"it": "Vuoi salvare?", "en": "Do you want to save?", "es": "¿Desea guardar?", "de": "Möchten Sie speichern?", "fr": "Voulez-vous enregistrer ?"},
    "Operation cancelled.": {"it": "Operazione annullata.", "en": "Operation cancelled.", "es": "Operación cancelada.", "de": "Vorgang abgebrochen.", "fr": "Opération annulée."},
    "Select an item!": {"it": "Seleziona un elemento!", "en": "Select an item!", "es": "¡Seleccione un elemento!", "de": "Artikel auswählen!", "fr": "Sélectionnez un élément !"},
    "Confirm deletion?": {"it": "Confermi eliminazione?", "en": "Confirm deletion?", "es": "¿Confirma eliminación?", "de": "Löschen bestätigen?", "fr": "Confirmer la suppression ?"},
    "Application restart is required to apply the new language.\n\nRestart now?": {"it": "È necessario riavviare l'applicazione per applicare la nuova lingua.\n\nRiavviare ora?", "en": "Application restart is required to apply the new language.\n\nRestart now?", "es": "Es necesario reiniciar la aplicación para aplicar el nuevo idioma.\n\n¿Reiniciar ahora?", "de": "Ein Neustart ist erforderlich, um die neue Sprache anzuwenden.\n\nJetzt neu starten?", "fr": "Un redémarrage est nécessaire pour appliquer la nouvelle langue.\n\nRedémarrer maintenant ?"},
    "Language changed": {"it": "Lingua cambiata", "en": "Language changed", "es": "Idioma cambiado", "de": "Sprache geändert", "fr": "Langue modifiée"},
    "Dates are not valid!": {"it": "Le date non sono valide!", "en": "Dates are not valid!", "es": "¡Las fechas no son válidas!", "de": "Daten sind ungültig!", "fr": "Les dates ne sont pas valides !"},
    "No data in selected period": {"it": "Nessun dato nel periodo selezionato", "en": "No data in selected period", "es": "Sin datos en el período seleccionado", "de": "Keine Daten im ausgewählten Zeitraum", "fr": "Aucune donnée dans la période sélectionnée"},
    "already exists!": {"it": "esiste già!", "en": "already exists!", "es": "¡ya existe!", "de": "existiert bereits!", "fr": "existe déjà !"},
    "is already assigned!": {"it": "è già assegnato!", "en": "is already assigned!", "es": "¡ya está asignado!", "de": "ist bereits zugewiesen!", "fr": "est déjà attribué !"},
    "Yes": {"it": "Sì", "en": "Yes", "es": "Sí", "de": "Ja", "fr": "Oui"},
    "No": {"it": "No", "en": "No", "es": "No", "de": "Nein", "fr": "Non"},

    # ==========================================================================
    # Menu - Purchases
    # ==========================================================================
    "Purchases": {"it": "Acquisti", "en": "Purchases", "es": "Compras", "de": "Einkäufe", "fr": "Achats"},
    "Deliberations": {"it": "Delibere", "en": "Deliberations", "es": "Deliberaciones", "de": "Beschlüsse", "fr": "Délibérations"},
    "Price List": {"it": "Listino Prezzi", "en": "Price List", "es": "Lista de Precios", "de": "Preisliste", "fr": "Liste de prix"},
    "Package Sources": {"it": "Fonti Package", "en": "Package Sources", "es": "Fuentes de Paquetes", "de": "Packungsquellen", "fr": "Sources de conditionnements"},
    "Package Funding Sources": {"it": "Fonti Finanziamento Packages", "en": "Package Funding Sources", "es": "Fuentes de Financiación de Paquetes", "de": "Packungsfinanzierungsquellen", "fr": "Sources de financement des conditionnements"},

    # ==========================================================================
    # Deliberations view
    # ==========================================================================
    "New Deliberation": {"it": "Nuova Delibera", "en": "New Deliberation", "es": "Nueva Deliberación", "de": "Neuer Beschluss", "fr": "Nouvelle délibération"},
    "Edit Deliberation": {"it": "Modifica Delibera", "en": "Edit Deliberation", "es": "Editar Deliberación", "de": "Beschluss bearbeiten", "fr": "Modifier la délibération"},
    "Number:": {"it": "Numero:", "en": "Number:", "es": "Número:", "de": "Nummer:", "fr": "Numéro :"},
    "Amount:": {"it": "Importo:", "en": "Amount:", "es": "Importe:", "de": "Betrag:", "fr": "Montant :"},
    "CIG:": {"it": "CIG:", "en": "CIG:", "es": "CIG:", "de": "CIG:", "fr": "CIG :"},
    "Active:": {"it": "Attiva:", "en": "Active:", "es": "Activa:", "de": "Aktiv:", "fr": "Actif :"},
    "Number field is required!": {"it": "Il campo Numero è obbligatorio!", "en": "Number field is required!", "es": "¡El campo Número es obligatorio!", "de": "Nummer-Feld ist erforderlich!", "fr": "Le champ Numéro est requis !"},
    "Amount": {"it": "Importo", "en": "Amount", "es": "Importe", "de": "Betrag", "fr": "Montant"},
    "CIG": {"it": "CIG", "en": "CIG", "es": "CIG", "de": "CIG", "fr": "CIG"},
    "Deliberation": {"it": "Delibera", "en": "Deliberation", "es": "Deliberación", "de": "Beschluss", "fr": "Délibération"},
    "Active": {"it": "Attive", "en": "Active", "es": "Activas", "de": "Aktiv", "fr": "Actifs"},
    "Number": {"it": "Numero", "en": "Number", "es": "Número", "de": "Nummer", "fr": "Numéro"},

    # ==========================================================================
    # Prices view
    # ==========================================================================
    "New Price": {"it": "Nuovo Prezzo", "en": "New Price", "es": "Nuevo Precio", "de": "Neuer Preis", "fr": "Nouveau prix"},
    "Edit Price": {"it": "Modifica Prezzo", "en": "Edit Price", "es": "Editar Precio", "de": "Preis bearbeiten", "fr": "Modifier le prix"},
    "Price:": {"it": "Prezzo:", "en": "Price:", "es": "Precio:", "de": "Preis:", "fr": "Prix :"},
    "Price": {"it": "Prezzo", "en": "Price", "es": "Precio", "de": "Preis", "fr": "Prix"},
    "VAT %:": {"it": "IVA %:", "en": "VAT %:", "es": "IVA %:", "de": "MwSt. %:", "fr": "TVA % :"},
    "VAT %": {"it": "IVA %", "en": "VAT %", "es": "IVA %", "de": "MwSt. %", "fr": "TVA %"},
    "Valid from:": {"it": "Valido dal:", "en": "Valid from:", "es": "Válido desde:", "de": "Gültig ab:", "fr": "Valide à partir de :"},
    "Valid from": {"it": "Valido dal", "en": "Valid from", "es": "Válido desde", "de": "Gültig ab", "fr": "Valide à partir de"},
    "Price field is required!": {"it": "Il campo Prezzo è obbligatorio!", "en": "Price field is required!", "es": "¡El campo Precio es obligatorio!", "de": "Preis-Feld ist erforderlich!", "fr": "Le champ Prix est requis !"},
    "Valid from field is required!": {"it": "Il campo Valido dal è obbligatorio!", "en": "Valid from field is required!", "es": "¡El campo Válido desde es obligatorio!", "de": "Gültig ab-Feld ist erforderlich!", "fr": "Le champ Valide à partir de est requis !"},

    # ==========================================================================
    # Package fundings view
    # ==========================================================================
    "New Funding Source": {"it": "Nuova Fonte Finanziamento", "en": "New Funding Source", "es": "Nueva Fuente de Financiación", "de": "Neue Finanzierungsquelle", "fr": "Nouvelle source de financement"},
    "Edit Funding Source": {"it": "Modifica Fonte Finanziamento", "en": "Edit Funding Source", "es": "Editar Fuente de Financiación", "de": "Finanzierungsquelle bearbeiten", "fr": "Modifier la source de financement"},
    "Product:": {"it": "Prodotto:", "en": "Product:", "es": "Producto:", "de": "Produkt:", "fr": "Produit :"},
    "Package:": {"it": "Package:", "en": "Package:", "es": "Paquete:", "de": "Packung:", "fr": "Conditionnement :"},
    "Funding Source:": {"it": "Fonte Finanziamento:", "en": "Funding Source:", "es": "Fuente de Financiación:", "de": "Finanzierungsquelle:", "fr": "Source de financement :"},
    "Select a Package!": {"it": "Selezionare un Package!", "en": "Select a Package!", "es": "¡Seleccione un Paquete!", "de": "Packung auswählen!", "fr": "Sélectionnez un conditionnement !"},
    "Select a Funding Source!": {"it": "Selezionare una Fonte Finanziamento!", "en": "Select a Funding Source!", "es": "¡Seleccione una Fuente de Financiación!", "de": "Finanzierungsquelle auswählen!", "fr": "Sélectionnez une source de financement !"},
    "Legend": {"it": "Legenda", "en": "Legend", "es": "Leyenda", "de": "Legende", "fr": "Légende"},
    "In Tender": {"it": "In Gara", "en": "In Tender", "es": "En Licitación", "de": "In Ausschreibung", "fr": "En appel d'offres"},
    "Direct Purchase": {"it": "Economia", "en": "Direct Purchase", "es": "Compra Directa", "de": "Direktkauf", "fr": "Achat direct"},
    "(optional - if in tender)": {"it": "(opzionale - se in gara)", "en": "(optional - if in tender)", "es": "(opcional - si en licitación)", "de": "(optional - falls in Ausschreibung)", "fr": "(optionnel - si en appel d'offres)"},
    "Sources/Delib.": {"it": "Fonti/Delibere", "en": "Sources/Delib.", "es": "Fuentes/Delib.", "de": "Quellen/Beschl.", "fr": "Sources/Délib."},
    "Search Package:": {"it": "Cerca Package:", "en": "Search Package:", "es": "Buscar Paquete:", "de": "Packung suchen:", "fr": "Rechercher conditionnement :"},
    "(description or code)": {"it": "(descrizione o codice)", "en": "(description or code)", "es": "(descripción o código)", "de": "(Beschreibung oder Code)", "fr": "(description ou code)"},
    "Results:": {"it": "Risultati:", "en": "Results:", "es": "Resultados:", "de": "Ergebnisse:", "fr": "Résultats :"},
    "Selected:": {"it": "Selezionato:", "en": "Selected:", "es": "Seleccionado:", "de": "Ausgewählt:", "fr": "Sélectionné :"},

    # ==========================================================================
    # Report Fundings
    # ==========================================================================
    "Funding Report": {"it": "Report Fonti", "en": "Funding Report", "es": "Informe de Fuentes", "de": "Finanzierungsbericht", "fr": "Rapport de financement"},
    "Funding Sources Report": {"it": "Report Fonti Finanziamento", "en": "Funding Sources Report", "es": "Informe de Fuentes de Financiación", "de": "Finanzierungsquellenbericht", "fr": "Rapport des sources de financement"},
    "No data to export!": {"it": "Nessun dato da esportare!", "en": "No data to export!", "es": "¡No hay datos para exportar!", "de": "Keine Daten zum Exportieren!", "fr": "Aucune donnée à exporter !"},
    "File exported": {"it": "File esportato", "en": "File exported", "es": "Archivo exportado", "de": "Datei exportiert", "fr": "Fichier exporté"},
    "Error during export": {"it": "Errore durante l'esportazione", "en": "Error during export", "es": "Error durante la exportación", "de": "Fehler beim Exportieren", "fr": "Erreur lors de l'exportation"},
    "Error during export": {"it": "Errore durante esportazione", "en": "Error during export", "es": "Error durante la exportación", "de": "Fehler beim Exportieren", "fr": "Erreur lors de l'exportation"},

    # ==========================================================================
    # Settings
    # ==========================================================================
    "Laboratory Settings": {"it": "Impostazioni Laboratorio", "en": "Laboratory Settings", "es": "Configuración del Laboratorio", "de": "Laboreinstellungen", "fr": "Paramètres du laboratoire"},
    "Hospital:": {"it": "Ospedale:", "en": "Hospital:", "es": "Hospital:", "de": "Krankenhaus:", "fr": "Hôpital :"},
    "Laboratory:": {"it": "Laboratorio:", "en": "Laboratory:", "es": "Laboratorio:", "de": "Labor:", "fr": "Laboratoire :"},
    "Manager:": {"it": "Responsabile:", "en": "Manager:", "es": "Responsable:", "de": "Leiter:", "fr": "Responsable :"},
    "Room/Location:": {"it": "Stanza/Locale:", "en": "Room/Location:", "es": "Sala/Local:", "de": "Raum/Standort:", "fr": "Salle/Emplacement :"},
    "Phone:": {"it": "Telefono:", "en": "Phone:", "es": "Teléfono:", "de": "Telefon:", "fr": "Téléphone :"},
    "Default VAT %:": {"it": "IVA predefinita %:", "en": "Default VAT %:", "es": "IVA predeterminado %:", "de": "Standard-MwSt. %:", "fr": "TVA par défaut % :"},
    "Idle timeout (min):": {"it": "Timeout inattività (min):", "en": "Idle timeout (min):", "es": "Tiempo de espera inactivo (min):", "de": "Leerlauf-Timeout (Min.):", "fr": "Délai d'inactivité (min) :"},
    "(0 = disabled)": {"it": "(0 = disabilitato)", "en": "(0 = disabled)", "es": "(0 = deshabilitado)", "de": "(0 = deaktiviert)", "fr": "(0 = désactivé)"},
    "Settings saved.": {"it": "Impostazioni salvate.", "en": "Settings saved.", "es": "Configuración guardada.", "de": "Einstellungen gespeichert.", "fr": "Paramètres enregistrés."},

    # ==========================================================================
    # Missing translations - Added batch
    # ==========================================================================
    "Action": {"it": "Azione", "en": "Action", "es": "Acción", "de": "Aktion", "fr": "Action"},
    "-- All categories --": {"it": "-- Tutte le categorie --", "en": "-- All categories --", "es": "-- Todas las categorías --", "de": "-- Alle Kategorien --", "fr": "-- Toutes les catégories --"},
    "All items have been delivered.": {"it": "Tutti gli articoli sono stati consegnati.", "en": "All items have been delivered.", "es": "Todos los artículos han sido entregados.", "de": "Alle Artikel wurden geliefert.", "fr": "Tous les articles ont été livrés."},
    "Already Delivered:": {"it": "Già consegnato:", "en": "Already Delivered:", "es": "Ya entregado:", "de": "Bereits geliefert:", "fr": "Déjà livré :"},
    "Application restart is required to apply the new language.\n\nRestart now?": {"it": "È necessario riavviare l'applicazione per applicare la nuova lingua.\n\nRiavviare ora?", "en": "Application restart is required to apply the new language.\n\nRestart now?", "es": "Es necesario reiniciar la aplicación para aplicar el nuevo idioma.\n\n¿Reiniciar ahora?", "de": "Ein Neustart der Anwendung ist erforderlich, um die neue Sprache anzuwenden.\n\nJetzt neu starten?", "fr": "Un redémarrage de l'application est nécessaire pour appliquer la nouvelle langue.\n\nRedémarrer maintenant ?"},
    "Avg stock TAT:": {"it": "TAT medio giacenza:", "en": "Avg stock TAT:", "es": "TAT medio stock:", "de": "Durchschn. Lager-TAT:", "fr": "TAT moyen stock :"},
    "Barcode Scanner": {"it": "Lettore Codice a Barre", "en": "Barcode Scanner", "es": "Escáner de Código de Barras", "de": "Barcode-Scanner", "fr": "Lecteur de code-barres"},
    "Batch '{}' already exists with expiration {}.\nInsert anyway with expiration {}?": {"it": "Il lotto '{}' esiste già con scadenza {}.\nInserire comunque con scadenza {}?", "en": "Batch '{}' already exists with expiration {}.\nInsert anyway with expiration {}?", "es": "El lote '{}' ya existe con vencimiento {}.\n¿Insertar de todos modos con vencimiento {}?", "de": "Charge '{}' existiert bereits mit Ablaufdatum {}.\nTrotzdem mit Ablaufdatum {} einfügen?", "fr": "Le lot '{}' existe déjà avec expiration {}.\nInsérer quand même avec expiration {} ?"},
    "Batch '{}' cancelled successfully.": {"it": "Lotto '{}' annullato con successo.", "en": "Batch '{}' cancelled successfully.", "es": "Lote '{}' cancelado con éxito.", "de": "Charge '{}' erfolgreich storniert.", "fr": "Lot '{}' annulé avec succès."},
    "Batch data not found!": {"it": "Dati lotto non trovati!", "en": "Batch data not found!", "es": "¡Datos del lote no encontrados!", "de": "Chargendaten nicht gefunden!", "fr": "Données du lot non trouvées !"},
    "Batch label:": {"it": "Etichetta lotto:", "en": "Batch label:", "es": "Etiqueta de lote:", "de": "Chargenetikett:", "fr": "Étiquette de lot :"},
    "Batch '{}' with expiration {} already exists!": {"it": "Il lotto '{}' con scadenza {} esiste già!", "en": "Batch '{}' with expiration {} already exists!", "es": "¡El lote '{}' con vencimiento {} ya existe!", "de": "Charge '{}' mit Ablaufdatum {} existiert bereits!", "fr": "Le lot '{}' avec expiration {} existe déjà !"},
    "By location (without stock)": {"it": "Per ubicazione (senza giacenza)", "en": "By location (without stock)", "es": "Por ubicación (sin stock)", "de": "Nach Standort (ohne Bestand)", "fr": "Par emplacement (sans stock)"},
    "By location (with stock)": {"it": "Per ubicazione (con giacenza)", "en": "By location (with stock)", "es": "Por ubicación (con stock)", "de": "Nach Standort (mit Bestand)", "fr": "Par emplacement (avec stock)"},
    "Cancel batch '{}' of '{}'?\n\n{} labels in stock will be cancelled.\n\nThis operation is not reversible.": {"it": "Annullare il lotto '{}' di '{}'?\n\n{} etichette in giacenza saranno annullate.\n\nQuesta operazione non è reversibile.", "en": "Cancel batch '{}' of '{}'?\n\n{} labels in stock will be cancelled.\n\nThis operation is not reversible.", "es": "¿Cancelar el lote '{}' de '{}'?\n\n{} etiquetas en stock serán canceladas.\n\nEsta operación no es reversible.", "de": "Charge '{}' von '{}' stornieren?\n\n{} Etiketten im Bestand werden storniert.\n\nDieser Vorgang ist nicht umkehrbar.", "fr": "Annuler le lot '{}' de '{}' ?\n\n{} étiquettes en stock seront annulées.\n\nCette opération n'est pas réversible."},
    "Cannot close the request.": {"it": "Impossibile chiudere la richiesta.", "en": "Cannot close the request.", "es": "No se puede cerrar la solicitud.", "de": "Anfrage kann nicht geschlossen werden.", "fr": "Impossible de fermer la demande."},
    "Category": {"it": "Categoria", "en": "Category", "es": "Categoría", "de": "Kategorie", "fr": "Catégorie"},
    "Commands": {"it": "Comandi", "en": "Commands", "es": "Comandos", "de": "Befehle", "fr": "Commandes"},
    "Compact (stock only)": {"it": "Compatto (solo giacenza)", "en": "Compact (stock only)", "es": "Compacto (solo stock)", "de": "Kompakt (nur Bestand)", "fr": "Compact (stock uniquement)"},
    "DDT:": {"it": "DDT:", "en": "DDT:", "es": "Albarán:", "de": "Lieferschein:", "fr": "Bon de livraison :"},
    "Del.": {"it": "Cons.", "en": "Del.", "es": "Entr.", "de": "Lief.", "fr": "Livr."},
    "Delete request '{}' and all its items?": {"it": "Eliminare la richiesta '{}' e tutti i suoi articoli?", "en": "Delete request '{}' and all its items?", "es": "¿Eliminar la solicitud '{}' y todos sus artículos?", "de": "Anfrage '{}' und alle zugehörigen Artikel löschen?", "fr": "Supprimer la demande '{}' et tous ses articles ?"},
    "Delete template '{}'?": {"it": "Eliminare il modello '{}'?", "en": "Delete template '{}'?", "es": "¿Eliminar la plantilla '{}'?", "de": "Vorlage '{}' löschen?", "fr": "Supprimer le modèle '{}' ?"},
    "Detailed (with batches)": {"it": "Dettagliato (con lotti)", "en": "Detailed (with batches)", "es": "Detallado (con lotes)", "de": "Detailliert (mit Chargen)", "fr": "Détaillé (avec lots)"},
    "Economy": {"it": "Economato", "en": "Economy", "es": "Economato", "de": "Wirtschaft", "fr": "Économat"},
    "Economy:": {"it": "Economato:", "en": "Economy:", "es": "Economato:", "de": "Wirtschaft:", "fr": "Économat :"},
    "Edit Resolution": {"it": "Modifica Delibera", "en": "Edit Resolution", "es": "Editar Resolución", "de": "Beschluss bearbeiten", "fr": "Modifier la délibération"},
    "Enter the DDT number!": {"it": "Inserire il numero DDT!", "en": "Enter the DDT number!", "es": "¡Ingrese el número de albarán!", "de": "Lieferscheinnummer eingeben!", "fr": "Entrez le numéro du bon de livraison !"},
    "Error printing:": {"it": "Errore di stampa:", "en": "Error printing:", "es": "Error de impresión:", "de": "Druckfehler:", "fr": "Erreur d'impression :"},
    "Execute": {"it": "Esegui", "en": "Execute", "es": "Ejecutar", "de": "Ausführen", "fr": "Exécuter"},
    "Expirations": {"it": "Scadenze", "en": "Expirations", "es": "Vencimientos", "de": "Ablaufdaten", "fr": "Expirations"},
    "Expiration status:": {"it": "Stato scadenza:", "en": "Expiration status:", "es": "Estado de vencimiento:", "de": "Ablaufstatus:", "fr": "État d'expiration :"},
    "=== Expired Batches ===": {"it": "=== Lotti Scaduti ===", "en": "=== Expired Batches ===", "es": "=== Lotes Vencidos ===", "de": "=== Abgelaufene Chargen ===", "fr": "=== Lots Expirés ==="},
    "EXPIRED by": {"it": "SCADUTO da", "en": "EXPIRED by", "es": "VENCIDO hace", "de": "ABGELAUFEN seit", "fr": "EXPIRÉ depuis"},
    "Expires in": {"it": "Scade tra", "en": "Expires in", "es": "Vence en", "de": "Läuft ab in", "fr": "Expire dans"},
    "Export Expirations": {"it": "Esporta Scadenze", "en": "Export Expirations", "es": "Exportar Vencimientos", "de": "Ablaufdaten exportieren", "fr": "Exporter les expirations"},
    "Export Suppliers": {"it": "Esporta Fornitori", "en": "Export Suppliers", "es": "Exportar Proveedores", "de": "Lieferanten exportieren", "fr": "Exporter les fournisseurs"},
    "Export TAT": {"it": "Esporta TAT", "en": "Export TAT", "es": "Exportar TAT", "de": "TAT exportieren", "fr": "Exporter TAT"},
    "=== FEFO Efficiency ===": {"it": "=== Efficienza FEFO ===", "en": "=== FEFO Efficiency ===", "es": "=== Eficiencia FEFO ===", "de": "=== FEFO-Effizienz ===", "fr": "=== Efficacité FEFO ==="},
    "Funding/Deliberations": {"it": "Fondi/Delibere", "en": "Funding/Deliberations", "es": "Fondos/Resoluciones", "de": "Finanzierung/Beschlüsse", "fr": "Financements/Délibérations"},
    "Fundings Report": {"it": "Report Fondi", "en": "Fundings Report", "es": "Informe de Fondos", "de": "Finanzierungsbericht", "fr": "Rapport des financements"},
    "Historical Expiration Analysis": {"it": "Analisi Storica Scadenze", "en": "Historical Expiration Analysis", "es": "Análisis Histórico de Vencimientos", "de": "Historische Ablaufanalyse", "fr": "Analyse historique des expirations"},
    "Info": {"it": "Info", "en": "Info", "es": "Info", "de": "Info", "fr": "Info"},
    "In stock": {"it": "In giacenza", "en": "In stock", "es": "En stock", "de": "Auf Lager", "fr": "En stock"},
    "In Tender:": {"it": "In gara:", "en": "In Tender:", "es": "En licitación:", "de": "In Ausschreibung:", "fr": "En appel d'offres :"},
    "Item Detail": {"it": "Dettaglio Articolo", "en": "Item Detail", "es": "Detalle del Artículo", "de": "Artikeldetail", "fr": "Détail de l'article"},
    "Items can only be modified in drafts!": {"it": "Gli articoli possono essere modificati solo nelle bozze!", "en": "Items can only be modified in drafts!", "es": "¡Los artículos solo pueden modificarse en borradores!", "de": "Artikel können nur in Entwürfen bearbeitet werden!", "fr": "Les articles ne peuvent être modifiés que dans les brouillons !"},
    "Items to Deliver": {"it": "Articoli da Consegnare", "en": "Items to Deliver", "es": "Artículos a Entregar", "de": "Zu liefernde Artikel", "fr": "Articles à livrer"},
    "Label Detail": {"it": "Dettaglio Etichetta", "en": "Label Detail", "es": "Detalle de Etiqueta", "de": "Etikettendetail", "fr": "Détail de l'étiquette"},
    "Label font:": {"it": "Font etichetta:", "en": "Label font:", "es": "Fuente de etiqueta:", "de": "Etikettenschrift:", "fr": "Police de l'étiquette :"},
    "Label {} has already been unloaded.\nUse 'Unload' to restore.": {"it": "L'etichetta {} è già stata scaricata.\nUsare 'Scarica' per ripristinare.", "en": "Label {} has already been unloaded.\nUse 'Unload' to restore.", "es": "La etiqueta {} ya ha sido descargada.\nUse 'Descargar' para restaurar.", "de": "Etikett {} wurde bereits entladen.\nVerwenden Sie 'Entladen' zum Wiederherstellen.", "fr": "L'étiquette {} a déjà été déchargée.\nUtilisez 'Décharger' pour restaurer."},
    "Label {} is already cancelled.\nRestore?": {"it": "L'etichetta {} è già annullata.\nRipristinare?", "en": "Label {} is already cancelled.\nRestore?", "es": "La etiqueta {} ya está cancelada.\n¿Restaurar?", "de": "Etikett {} ist bereits storniert.\nWiederherstellen?", "fr": "L'étiquette {} est déjà annulée.\nRestaurer ?"},
    "Label Printing:": {"it": "Stampa Etichette:", "en": "Label Printing:", "es": "Impresión de Etiquetas:", "de": "Etikettendruck:", "fr": "Impression d'étiquettes :"},
    "labels": {"it": "etichette", "en": "labels", "es": "etiquetas", "de": "Etiketten", "fr": "étiquettes"},
    "Labels:": {"it": "Etichette:", "en": "Labels:", "es": "Etiquetas:", "de": "Etiketten:", "fr": "Étiquettes :"},
    "Labels created but error printing:": {"it": "Etichette create ma errore di stampa:", "en": "Labels created but error printing:", "es": "Etiquetas creadas pero error de impresión:", "de": "Etiketten erstellt, aber Druckfehler:", "fr": "Étiquettes créées mais erreur d'impression :"},
    "Label sent to printer!": {"it": "Etichetta inviata alla stampante!", "en": "Label sent to printer!", "es": "¡Etiqueta enviada a la impresora!", "de": "Etikett an Drucker gesendet!", "fr": "Étiquette envoyée à l'imprimante !"},
    "Labels per unit:": {"it": "Etichette per unità:", "en": "Labels per unit:", "es": "Etiquetas por unidad:", "de": "Etiketten pro Einheit:", "fr": "Étiquettes par unité :"},
    "Labels Unloaded": {"it": "Etichette Scaricate", "en": "Labels Unloaded", "es": "Etiquetas Descargadas", "de": "Etiketten entladen", "fr": "Étiquettes déchargées"},
    "Language:": {"it": "Lingua:", "en": "Language:", "es": "Idioma:", "de": "Sprache:", "fr": "Langue :"},
    "Language changed. Restart application to apply?": {"it": "Lingua cambiata. Riavviare l'applicazione per applicare?", "en": "Language changed. Restart application to apply?", "es": "Idioma cambiado. ¿Reiniciar la aplicación para aplicar?", "de": "Sprache geändert. Anwendung neu starten, um anzuwenden?", "fr": "Langue modifiée. Redémarrer l'application pour appliquer ?"},
    "Loaded on:": {"it": "Caricato il:", "en": "Loaded on:", "es": "Cargado el:", "de": "Geladen am:", "fr": "Chargé le :"},
    "Load {} label?": {"it": "Caricare {} etichetta?", "en": "Load {} label?", "es": "¿Cargar {} etiqueta?", "de": "{} Etikett laden?", "fr": "Charger {} étiquette ?"},
    "Load {} labels?": {"it": "Caricare {} etichette?", "en": "Load {} labels?", "es": "¿Cargar {} etiquetas?", "de": "{} Etiketten laden?", "fr": "Charger {} étiquettes ?"},
    "Local Settings": {"it": "Impostazioni Locali", "en": "Local Settings", "es": "Configuración Local", "de": "Lokale Einstellungen", "fr": "Paramètres locaux"},
    "Lot": {"it": "Lotto", "en": "Lot", "es": "Lote", "de": "Charge", "fr": "Lot"},
    "Lot Label": {"it": "Etichetta Lotto", "en": "Lot Label", "es": "Etiqueta de Lote", "de": "Chargenetikett", "fr": "Étiquette de lot"},
    "New Resolution": {"it": "Nuova Delibera", "en": "New Resolution", "es": "Nueva Resolución", "de": "Neuer Beschluss", "fr": "Nouvelle délibération"},
    "No data in the selected period": {"it": "Nessun dato nel periodo selezionato", "en": "No data in the selected period", "es": "Sin datos en el período seleccionado", "de": "Keine Daten im ausgewählten Zeitraum", "fr": "Aucune donnée dans la période sélectionnée"},
    "No expiration": {"it": "Senza scadenza", "en": "No expiration", "es": "Sin vencimiento", "de": "Kein Ablaufdatum", "fr": "Sans expiration"},
    "No more active items.": {"it": "Nessun altro articolo attivo.", "en": "No more active items.", "es": "No hay más artículos activos.", "de": "Keine weiteren aktiven Artikel.", "fr": "Plus d'articles actifs."},
    "-- Non assegnata --": {"it": "-- Non assegnata --", "en": "-- Not assigned --", "es": "-- Sin asignar --", "de": "-- Nicht zugewiesen --", "fr": "-- Non assignée --"},
    "-- Non assegnato --": {"it": "-- Non assegnato --", "en": "-- Not assigned --", "es": "-- Sin asignar --", "de": "-- Nicht zugewiesen --", "fr": "-- Non assigné --"},
    "No products found for the selected category.": {"it": "Nessun prodotto trovato per la categoria selezionata.", "en": "No products found for the selected category.", "es": "No se encontraron productos para la categoría seleccionada.", "de": "Keine Produkte für die ausgewählte Kategorie gefunden.", "fr": "Aucun produit trouvé pour la catégorie sélectionnée."},
    "No products found for the selected location.": {"it": "Nessun prodotto trovato per l'ubicazione selezionata.", "en": "No products found for the selected location.", "es": "No se encontraron productos para la ubicación seleccionada.", "de": "Keine Produkte für den ausgewählten Standort gefunden.", "fr": "Aucun produit trouvé pour l'emplacement sélectionné."},
    "Options": {"it": "Opzioni", "en": "Options", "es": "Opciones", "de": "Optionen", "fr": "Options"},
    "Ordered:": {"it": "Ordinato:", "en": "Ordered:", "es": "Pedido:", "de": "Bestellt:", "fr": "Commandé :"},
    "=== Order TAT ===": {"it": "=== TAT Ordini ===", "en": "=== Order TAT ===", "es": "=== TAT de Pedidos ===", "de": "=== Bestell-TAT ===", "fr": "=== TAT Commandes ==="},
    "Package Fundings": {"it": "Fondi Pacchetto", "en": "Package Fundings", "es": "Fondos del Paquete", "de": "Paketfinanzierung", "fr": "Financements du paquet"},
    "Please enter at least one line of text!": {"it": "Inserire almeno una riga di testo!", "en": "Please enter at least one line of text!", "es": "¡Ingrese al menos una línea de texto!", "de": "Bitte mindestens eine Textzeile eingeben!", "fr": "Veuillez entrer au moins une ligne de texte !"},
    "Please enter at least the first line!": {"it": "Inserire almeno la prima riga!", "en": "Please enter at least the first line!", "es": "¡Ingrese al menos la primera línea!", "de": "Bitte mindestens die erste Zeile eingeben!", "fr": "Veuillez entrer au moins la première ligne !"},
    "Please enter the cancellation reason!": {"it": "Inserire il motivo dell'annullamento!", "en": "Please enter the cancellation reason!", "es": "¡Ingrese el motivo de la cancelación!", "de": "Bitte den Stornierungsgrund eingeben!", "fr": "Veuillez entrer le motif d'annulation !"},
    "Please select a category!": {"it": "Selezionare una categoria!", "en": "Please select a category!", "es": "¡Seleccione una categoría!", "de": "Bitte eine Kategorie auswählen!", "fr": "Veuillez sélectionner une catégorie !"},
    "Please select a Funding Source!": {"it": "Selezionare una fonte di finanziamento!", "en": "Please select a Funding Source!", "es": "¡Seleccione una fuente de financiación!", "de": "Bitte eine Finanzierungsquelle auswählen!", "fr": "Veuillez sélectionner une source de financement !"},
    "Please select a location!": {"it": "Selezionare un'ubicazione!", "en": "Please select a location!", "es": "¡Seleccione una ubicación!", "de": "Bitte einen Standort auswählen!", "fr": "Veuillez sélectionner un emplacement !"},
    "Please select a package!": {"it": "Selezionare un pacchetto!", "en": "Please select a package!", "es": "¡Seleccione un paquete!", "de": "Bitte ein Paket auswählen!", "fr": "Veuillez sélectionner un paquet !"},
    "Please select a Package!": {"it": "Selezionare un Pacchetto!", "en": "Please select a Package!", "es": "¡Seleccione un Paquete!", "de": "Bitte ein Paket auswählen!", "fr": "Veuillez sélectionner un Paquet !"},
    "Please select a product!": {"it": "Selezionare un prodotto!", "en": "Please select a product!", "es": "¡Seleccione un producto!", "de": "Bitte ein Produkt auswählen!", "fr": "Veuillez sélectionner un produit !"},
    "Please select a Supplier!": {"it": "Selezionare un fornitore!", "en": "Please select a Supplier!", "es": "¡Seleccione un proveedor!", "de": "Bitte einen Lieferanten auswählen!", "fr": "Veuillez sélectionner un fournisseur !"},
    "Print labels": {"it": "Stampa etichette", "en": "Print labels", "es": "Imprimir etiquetas", "de": "Etiketten drucken", "fr": "Imprimer les étiquettes"},
    "Product code:": {"it": "Codice prodotto:", "en": "Product code:", "es": "Código de producto:", "de": "Produktcode:", "fr": "Code produit :"},
    "Request Detail": {"it": "Dettaglio Richiesta", "en": "Request Detail", "es": "Detalle de Solicitud", "de": "Anfragedetail", "fr": "Détail de la demande"},
    "Resolution": {"it": "Delibera", "en": "Resolution", "es": "Resolución", "de": "Beschluss", "fr": "Délibération"},
    "Resolution:": {"it": "Delibera:", "en": "Resolution:", "es": "Resolución:", "de": "Beschluss:", "fr": "Délibération :"},
    "Resolutions": {"it": "Delibere", "en": "Resolutions", "es": "Resoluciones", "de": "Beschlüsse", "fr": "Délibérations"},
    "Select an element!": {"it": "Selezionare un elemento!", "en": "Select an element!", "es": "¡Seleccione un elemento!", "de": "Bitte ein Element auswählen!", "fr": "Veuillez sélectionner un élément !"},
    "Select an item to deliver!": {"it": "Selezionare un articolo da consegnare!", "en": "Select an item to deliver!", "es": "¡Seleccione un artículo a entregar!", "de": "Bitte einen zu liefernden Artikel auswählen!", "fr": "Veuillez sélectionner un article à livrer !"},
    "Send": {"it": "Invia", "en": "Send", "es": "Enviar", "de": "Senden", "fr": "Envoyer"},
    "Shelf:": {"it": "Scaffale:", "en": "Shelf:", "es": "Estante:", "de": "Regal:", "fr": "Étagère :"},
    "Stk": {"it": "Giac", "en": "Stk", "es": "Stk", "de": "Bst", "fr": "Stk"},
    "=== Stock TAT ===": {"it": "=== TAT Giacenza ===", "en": "=== Stock TAT ===", "es": "=== TAT de Stock ===", "de": "=== Lager-TAT ===", "fr": "=== TAT Stock ==="},
    "Stock Time (Loading → Unloading)": {"it": "Tempo Giacenza (Carico → Scarico)", "en": "Stock Time (Loading → Unloading)", "es": "Tiempo de Stock (Carga → Descarga)", "de": "Lagerzeit (Laden → Entladen)", "fr": "Temps de stock (Chargement → Déchargement)"},
    "Supplier code:": {"it": "Codice fornitore:", "en": "Supplier code:", "es": "Código de proveedor:", "de": "Lieferantencode:", "fr": "Code fournisseur :"},
    "Template '{}' exists.\nOverwrite?": {"it": "Il modello '{}' esiste.\nSovrascrivere?", "en": "Template '{}' exists.\nOverwrite?", "es": "La plantilla '{}' existe.\n¿Sobrescribir?", "de": "Vorlage '{}' existiert.\nÜberschreiben?", "fr": "Le modèle '{}' existe.\nÉcraser ?"},
    "Template '{}' saved!": {"it": "Modello '{}' salvato!", "en": "Template '{}' saved!", "es": "¡Plantilla '{}' guardada!", "de": "Vorlage '{}' gespeichert!", "fr": "Modèle '{}' enregistré !"},
    "The Batch field is required!": {"it": "Il campo Lotto è obbligatorio!", "en": "The Batch field is required!", "es": "¡El campo Lote es obligatorio!", "de": "Das Feld Charge ist erforderlich!", "fr": "Le champ Lot est requis !"},
    "The batch has already expired!\nCannot insert.": {"it": "Il lotto è già scaduto!\nImpossibile inserire.", "en": "The batch has already expired!\nCannot insert.", "es": "¡El lote ya ha vencido!\nNo se puede insertar.", "de": "Die Charge ist bereits abgelaufen!\nEinfügen nicht möglich.", "fr": "Le lot a déjà expiré !\nImpossible d'insérer."},
    "The category '{}' already exists!": {"it": "La categoria '{}' esiste già!", "en": "The category '{}' already exists!", "es": "¡La categoría '{}' ya existe!", "de": "Die Kategorie '{}' existiert bereits!", "fr": "La catégorie '{}' existe déjà !"},
    "The Code field is required!": {"it": "Il campo Codice è obbligatorio!", "en": "The Code field is required!", "es": "¡El campo Código es obligatorio!", "de": "Das Feld Code ist erforderlich!", "fr": "Le champ Code est requis !"},
    "The code '{}' is already assigned!": {"it": "Il codice '{}' è già assegnato!", "en": "The code '{}' is already assigned!", "es": "¡El código '{}' ya está asignado!", "de": "Der Code '{}' ist bereits vergeben!", "fr": "Le code '{}' est déjà attribué !"},
    "The dates are not valid!": {"it": "Le date non sono valide!", "en": "The dates are not valid!", "es": "¡Las fechas no son válidas!", "de": "Die Daten sind ungültig!", "fr": "Les dates ne sont pas valides !"},
    "The Description field is required!": {"it": "Il campo Descrizione è obbligatorio!", "en": "The Description field is required!", "es": "¡El campo Descripción es obligatorio!", "de": "Das Feld Beschreibung ist erforderlich!", "fr": "Le champ Description est requis !"},
    "The Number field is required!": {"it": "Il campo Numero è obbligatorio!", "en": "The Number field is required!", "es": "¡El campo Número es obligatorio!", "de": "Das Feld Nummer ist erforderlich!", "fr": "Le champ Numéro est requis !"},
    "The Price field is required!": {"it": "Il campo Prezzo è obbligatorio!", "en": "The Price field is required!", "es": "¡El campo Precio es obligatorio!", "de": "Das Feld Preis ist erforderlich!", "fr": "Le champ Prix est requis !"},
    "The product '{}' already exists!": {"it": "Il prodotto '{}' esiste già!", "en": "The product '{}' already exists!", "es": "¡El producto '{}' ya existe!", "de": "Das Produkt '{}' existiert bereits!", "fr": "Le produit '{}' existe déjà !"},
    "There are {} items not fully delivered.": {"it": "Ci sono {} articoli non completamente consegnati.", "en": "There are {} items not fully delivered.", "es": "Hay {} artículos no completamente entregados.", "de": "Es gibt {} nicht vollständig gelieferte Artikel.", "fr": "Il y a {} articles non entièrement livrés."},
    "The resolution '{}' already exists!": {"it": "La delibera '{}' esiste già!", "en": "The resolution '{}' already exists!", "es": "¡La resolución '{}' ya existe!", "de": "Der Beschluss '{}' existiert bereits!", "fr": "La délibération '{}' existe déjà !"},
    "The storage condition '{}' already exists!": {"it": "La modalità di conservazione '{}' esiste già!", "en": "The storage condition '{}' already exists!", "es": "¡La condición de almacenamiento '{}' ya existe!", "de": "Die Lagerbedingung '{}' existiert bereits!", "fr": "La condition de stockage '{}' existe déjà !"},
    "The supplier '{}' already exists!": {"it": "Il fornitore '{}' esiste già!", "en": "The supplier '{}' already exists!", "es": "¡El proveedor '{}' ya existe!", "de": "Der Lieferant '{}' existiert bereits!", "fr": "Le fournisseur '{}' existe déjà !"},
    "The Valid from field is required!": {"it": "Il campo Valido dal è obbligatorio!", "en": "The Valid from field is required!", "es": "¡El campo Válido desde es obligatorio!", "de": "Das Feld Gültig ab ist erforderlich!", "fr": "Le champ Valide à partir de est requis !"},
    "Unable to create the database.": {"it": "Impossibile creare il database.", "en": "Unable to create the database.", "es": "No se puede crear la base de datos.", "de": "Datenbank kann nicht erstellt werden.", "fr": "Impossible de créer la base de données."},
    "Unknown": {"it": "Sconosciuto", "en": "Unknown", "es": "Desconocido", "de": "Unbekannt", "fr": "Inconnu"},
    "Unloaded on:": {"it": "Scaricato il:", "en": "Unloaded on:", "es": "Descargado el:", "de": "Entladen am:", "fr": "Déchargé le :"},
    "Warning: the batch expires in {} days.\nProceed anyway?": {"it": "Attenzione: il lotto scade tra {} giorni.\nProcedere comunque?", "en": "Warning: the batch expires in {} days.\nProceed anyway?", "es": "Advertencia: el lote vence en {} días.\n¿Continuar de todos modos?", "de": "Warnung: Die Charge läuft in {} Tagen ab.\nTrotzdem fortfahren?", "fr": "Attention : le lot expire dans {} jours.\nContinuer quand même ?"},

    # ==========================================================================
    # Memos view
    # ==========================================================================
    "Memos": {"it": "Promemoria", "en": "Memos", "es": "Notas", "de": "Notizen", "fr": "Mémos"},
    "Add": {"it": "Aggiungi", "en": "Add", "es": "Añadir", "de": "Hinzufügen", "fr": "Ajouter"},
    "Done": {"it": "Fatto", "en": "Done", "es": "Hecho", "de": "Erledigt", "fr": "Terminé"},
    "Show completed": {"it": "Mostra completati", "en": "Show completed", "es": "Mostrar completados", "de": "Erledigte anzeigen", "fr": "Afficher terminés"},
    "Delete this memo?": {"it": "Eliminare questo promemoria?", "en": "Delete this memo?", "es": "¿Eliminar esta nota?", "de": "Diese Notiz löschen?", "fr": "Supprimer ce mémo ?"},
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
