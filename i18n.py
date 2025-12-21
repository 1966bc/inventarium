# -*- coding: utf-8 -*-
"""
Internationalization Module for Inventarium.

Provides translation support for Italian, English and Spanish languages.

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""

# Available languages
LANGUAGES = {
    "it": "Italiano",
    "en": "English",
    "es": "Español"
}

# Default language
DEFAULT_LANGUAGE = "it"

# Translation dictionary
TRANSLATIONS = {
    # ==========================================================================
    # Menu - File
    # ==========================================================================
    "File": {"it": "File", "en": "File", "es": "Archivo"},
    "Impostazioni": {"it": "Impostazioni", "en": "Settings", "es": "Configuración"},
    "Configura Database": {"it": "Configura Database", "en": "Configure Database", "es": "Configurar Base de Datos"},
    "Database": {"it": "Database", "en": "Database", "es": "Base de Datos"},
    "Configura": {"it": "Configura", "en": "Configure", "es": "Configurar"},
    "Backup": {"it": "Backup", "en": "Backup", "es": "Copia de Seguridad"},
    "Compatta": {"it": "Compatta", "en": "Compact", "es": "Compactar"},
    "Backup Database": {"it": "Backup Database", "en": "Backup Database", "es": "Copia de Seguridad"},
    "Compatta Database": {"it": "Compatta Database", "en": "Compact Database", "es": "Compactar Base de Datos"},
    "Database compattato!": {"it": "Database compattato!", "en": "Database compacted!", "es": "¡Base de datos compactada!"},
    "Prima": {"it": "Prima", "en": "Before", "es": "Antes"},
    "Dopo": {"it": "Dopo", "en": "After", "es": "Después"},
    "Risparmiato": {"it": "Risparmiato", "en": "Saved", "es": "Ahorrado"},
    "Errore durante la compattazione": {"it": "Errore durante la compattazione", "en": "Error during compaction", "es": "Error durante la compactación"},
    "Log": {"it": "Log", "en": "Log", "es": "Registro"},
    "Etichetta Personalizzata": {"it": "Etichetta Personalizzata", "en": "Custom Label", "es": "Etiqueta Personalizada"},
    "Esci": {"it": "Esci", "en": "Exit", "es": "Salir"},
    "Lingua": {"it": "Lingua", "en": "Language", "es": "Idioma"},

    # ==========================================================================
    # Menu - Warehouse
    # ==========================================================================
    "Magazzino": {"it": "Magazzino", "en": "Warehouse", "es": "Almacén"},
    "Giacenze": {"it": "Giacenze", "en": "Stock", "es": "Existencias"},
    "Stampa Giacenze": {"it": "Stampa Giacenze", "en": "Print Stock", "es": "Imprimir Existencias"},
    "Scarico": {"it": "Scarico", "en": "Unload", "es": "Descarga"},
    "Scadenze": {"it": "Scadenze", "en": "Expiring", "es": "Caducidades"},

    # ==========================================================================
    # Menu - Requests
    # ==========================================================================
    "Richieste": {"it": "Richieste", "en": "Requests", "es": "Solicitudes"},
    "Consegne": {"it": "Consegne", "en": "Deliveries", "es": "Entregas"},

    # ==========================================================================
    # Menu - Admin
    # ==========================================================================
    "Anagrafiche": {"it": "Anagrafiche", "en": "Master Data", "es": "Datos Maestros"},
    "Prodotti": {"it": "Prodotti", "en": "Products", "es": "Productos"},
    "Fornitori": {"it": "Fornitori", "en": "Suppliers", "es": "Proveedores"},
    "Categorie": {"it": "Categorie", "en": "Categories", "es": "Categorías"},
    "Conservazioni": {"it": "Conservazioni", "en": "Storage Conditions", "es": "Condiciones de Almacenamiento"},
    "Ubicazioni": {"it": "Ubicazioni", "en": "Locations", "es": "Ubicaciones"},
    "Fonti Finanziamento": {"it": "Fonti Finanziamento", "en": "Funding Sources", "es": "Fuentes de Financiación"},
    "Fonti di Finanziamento": {"it": "Fonti di Finanziamento", "en": "Funding Sources", "es": "Fuentes de Financiación"},
    "Totale": {"it": "Totale", "en": "Total", "es": "Total"},

    # ==========================================================================
    # Menu - Statistics
    # ==========================================================================
    "Statistiche": {"it": "Statistiche", "en": "Statistics", "es": "Estadísticas"},
    "Dashboard": {"it": "Dashboard", "en": "Dashboard", "es": "Panel de Control"},
    "Consumi": {"it": "Consumi", "en": "Consumption", "es": "Consumos"},
    "Rotazione": {"it": "Rotazione", "en": "Rotation", "es": "Rotación"},
    "Tempi (TAT)": {"it": "Tempi (TAT)", "en": "Times (TAT)", "es": "Tiempos (TAT)"},

    # ==========================================================================
    # Menu - Help
    # ==========================================================================
    "Informazioni": {"it": "Informazioni", "en": "About", "es": "Acerca de"},
    "Licenza": {"it": "Licenza", "en": "License", "es": "Licencia"},
    "Versione Python": {"it": "Versione Python", "en": "Python Version", "es": "Versión de Python"},
    "Versione Tkinter": {"it": "Versione Tkinter", "en": "Tkinter Version", "es": "Versión de Tkinter"},

    # ==========================================================================
    # Common buttons
    # ==========================================================================
    "Salva": {"it": "Salva", "en": "Save", "es": "Guardar"},
    "Chiudi": {"it": "Chiudi", "en": "Close", "es": "Cerrar"},
    "Annulla": {"it": "Annulla", "en": "Cancel", "es": "Cancelar"},
    "Nuovo": {"it": "Nuovo", "en": "New", "es": "Nuevo"},
    "Modifica": {"it": "Modifica", "en": "Edit", "es": "Editar"},
    "Elimina": {"it": "Elimina", "en": "Delete", "es": "Eliminar"},
    "Cerca": {"it": "Cerca", "en": "Search", "es": "Buscar"},
    "Aggiorna": {"it": "Aggiorna", "en": "Refresh", "es": "Actualizar"},
    "Stampa": {"it": "Stampa", "en": "Print", "es": "Imprimir"},
    "Esporta CSV": {"it": "Esporta CSV", "en": "Export CSV", "es": "Exportar CSV"},
    "Scarica": {"it": "Scarica", "en": "Unload", "es": "Descargar"},
    "Annulla Lotto": {"it": "Annulla Lotto", "en": "Cancel Batch", "es": "Cancelar Lote"},
    "Calcola": {"it": "Calcola", "en": "Calculate", "es": "Calcular"},
    "Carica": {"it": "Carica", "en": "Load", "es": "Cargar"},
    "Anteprima": {"it": "Anteprima", "en": "Preview", "es": "Vista Previa"},
    "Dettagli": {"it": "Dettagli", "en": "Details", "es": "Detalles"},
    "Storico": {"it": "Storico", "en": "History", "es": "Historial"},
    "Nuovo Lotto": {"it": "Nuovo Lotto", "en": "New Batch", "es": "Nuevo Lote"},
    "Carica Etichette": {"it": "Carica Etichette", "en": "Load Labels", "es": "Cargar Etiquetas"},
    "Confezioni": {"it": "Confezioni", "en": "Packages", "es": "Envases"},
    "Genera": {"it": "Genera", "en": "Generate", "es": "Generar"},

    # ==========================================================================
    # Common labels
    # ==========================================================================
    "Descrizione:": {"it": "Descrizione:", "en": "Description:", "es": "Descripción:"},
    "Codice:": {"it": "Codice:", "en": "Code:", "es": "Código:"},
    "Attivo:": {"it": "Attivo:", "en": "Active:", "es": "Activo:"},
    "Stato": {"it": "Stato", "en": "Status", "es": "Estado"},
    "Attivi": {"it": "Attivi", "en": "Active", "es": "Activos"},
    "Non Attivi": {"it": "Non Attivi", "en": "Inactive", "es": "Inactivos"},
    "Tutti": {"it": "Tutti", "en": "All", "es": "Todos"},
    "Ricerca": {"it": "Ricerca", "en": "Search", "es": "Búsqueda"},
    "Totale:": {"it": "Totale:", "en": "Total:", "es": "Total:"},
    "Da:": {"it": "Da:", "en": "From:", "es": "Desde:"},
    "A:": {"it": "A:", "en": "To:", "es": "Hasta:"},
    "Periodo rapido:": {"it": "Periodo rapido:", "en": "Quick period:", "es": "Período rápido:"},
    "Tipo": {"it": "Tipo", "en": "Type", "es": "Tipo"},
    "Descrizione": {"it": "Descrizione", "en": "Description", "es": "Descripción"},
    "Codice": {"it": "Codice", "en": "Code", "es": "Código"},

    # ==========================================================================
    # Warehouse view
    # ==========================================================================
    "Prodotto": {"it": "Prodotto", "en": "Product", "es": "Producto"},
    "Lotto": {"it": "Lotto", "en": "Batch", "es": "Lote"},
    "Lotti": {"it": "Lotti", "en": "Batches", "es": "Lotes"},
    "Scadenza": {"it": "Scadenza", "en": "Expiration", "es": "Caducidad"},
    "Etichette": {"it": "Etichette", "en": "Labels", "es": "Etiquetas"},
    "Azione etichetta": {"it": "Azione etichetta", "en": "Label action", "es": "Acción de etiqueta"},
    "Evadi": {"it": "Evadi", "en": "Dispatch", "es": "Despachar"},
    "Prodotti (selezionare categoria)": {"it": "Prodotti (selezionare categoria)", "en": "Products (select category)", "es": "Productos (seleccionar categoría)"},
    "-- Tutte --": {"it": "-- Tutte --", "en": "-- All --", "es": "-- Todas --"},
    "Dettagli Prodotto": {"it": "Dettagli Prodotto", "en": "Product Details", "es": "Detalles del Producto"},
    "Fornitore:": {"it": "Fornitore:", "en": "Supplier:", "es": "Proveedor:"},
    "Confezionamento:": {"it": "Confezionamento:", "en": "Packaging:", "es": "Envase:"},
    "Conservazione:": {"it": "Conservazione:", "en": "Storage:", "es": "Conservación:"},
    "Al buio:": {"it": "Al buio:", "en": "In dark:", "es": "En oscuridad:"},
    "Categoria:": {"it": "Categoria:", "en": "Category:", "es": "Categoría:"},
    "Giacenza:": {"it": "Giacenza:", "en": "Stock:", "es": "Existencias:"},
    "Selezionare un prodotto!": {"it": "Selezionare un prodotto!", "en": "Select a product!", "es": "¡Seleccione un producto!"},
    "Selezionare un lotto!": {"it": "Selezionare un lotto!", "en": "Select a batch!", "es": "¡Seleccione un lote!"},
    "Scaricare l'etichetta": {"it": "Scaricare l'etichetta", "en": "Unload label", "es": "Descargar etiqueta"},
    "Ripristinare l'etichetta": {"it": "Ripristinare l'etichetta", "en": "Restore label", "es": "Restaurar etiqueta"},
    "Annullare l'etichetta": {"it": "Annullare l'etichetta", "en": "Cancel label", "es": "Cancelar etiqueta"},
    "Etichetta generata e inviata alla stampa.": {"it": "Etichetta generata e inviata alla stampa.", "en": "Label generated and sent to print.", "es": "Etiqueta generada y enviada a imprimir."},
    "Errore nella generazione dell'etichetta:": {"it": "Errore nella generazione dell'etichetta:", "en": "Error generating label:", "es": "Error al generar la etiqueta:"},

    # ==========================================================================
    # Products view
    # ==========================================================================
    "Nuovo Prodotto": {"it": "Nuovo Prodotto", "en": "New Product", "es": "Nuevo Producto"},
    "Modifica Prodotto": {"it": "Modifica Prodotto", "en": "Edit Product", "es": "Editar Producto"},
    "Il campo Codice è obbligatorio!": {"it": "Il campo Codice è obbligatorio!", "en": "Code field is required!", "es": "¡El campo Código es obligatorio!"},
    "Il campo Descrizione è obbligatorio!": {"it": "Il campo Descrizione è obbligatorio!", "en": "Description field is required!", "es": "¡El campo Descripción es obligatorio!"},

    # ==========================================================================
    # Packages view
    # ==========================================================================
    "Nuova Confezione": {"it": "Nuova Confezione", "en": "New Package", "es": "Nuevo Envase"},
    "Modifica Confezione": {"it": "Modifica Confezione", "en": "Edit Package", "es": "Editar Envase"},
    "Cod.Forn.": {"it": "Cod.Forn.", "en": "Supp.Code", "es": "Cód.Prov."},
    "Fornitore": {"it": "Fornitore", "en": "Supplier", "es": "Proveedor"},
    "Et.": {"it": "Et.", "en": "Lb.", "es": "Etiq."},
    "Confezionamento": {"it": "Confezionamento", "en": "Packaging", "es": "Envase"},
    "Conserv.": {"it": "Conserv.", "en": "Storage", "es": "Conserv."},
    "Fonte": {"it": "Fonte", "en": "Source", "es": "Fuente"},
    "Cod. Fornitore:": {"it": "Cod. Fornitore:", "en": "Supplier Code:", "es": "Código Proveedor:"},
    "Ubicazione": {"it": "Ubicazione", "en": "Location", "es": "Ubicación"},
    "Ubicazione:": {"it": "Ubicazione:", "en": "Location:", "es": "Ubicación:"},
    "Fonte:": {"it": "Fonte:", "en": "Source:", "es": "Fuente:"},
    "Ordinazione:": {"it": "Ordinazione:", "en": "Ordering:", "es": "Pedido:"},
    "Al pezzo": {"it": "Al pezzo", "en": "By piece", "es": "Por unidad"},
    "A confezione": {"it": "A confezione", "en": "By package", "es": "Por envase"},
    "Pezzi per etichetta:": {"it": "Pezzi per etichetta:", "en": "Pieces per label:", "es": "Piezas por etiqueta:"},
    "Soglia riordino:": {"it": "Soglia riordino:", "en": "Reorder level:", "es": "Nivel de reorden:"},
    "-- Non assegnata --": {"it": "-- Non assegnata --", "en": "-- Not assigned --", "es": "-- Sin asignar --"},
    "Selezionare un fornitore!": {"it": "Selezionare un fornitore!", "en": "Select a supplier!", "es": "¡Seleccione un proveedor!"},
    "Il campo Codice Fornitore è obbligatorio!": {"it": "Il campo Codice Fornitore è obbligatorio!", "en": "Supplier Code field is required!", "es": "¡El campo Código Proveedor es obligatorio!"},
    "Il campo Confezionamento è obbligatorio!": {"it": "Il campo Confezionamento è obbligatorio!", "en": "Packaging field is required!", "es": "¡El campo Envase es obligatorio!"},
    "Selezionare una modalità di conservazione!": {"it": "Selezionare una modalità di conservazione!", "en": "Select a storage condition!", "es": "¡Seleccione una condición de almacenamiento!"},

    # ==========================================================================
    # Suppliers view
    # ==========================================================================
    "Nuovo Fornitore": {"it": "Nuovo Fornitore", "en": "New Supplier", "es": "Nuevo Proveedor"},
    "Modifica Fornitore": {"it": "Modifica Fornitore", "en": "Edit Supplier", "es": "Editar Proveedor"},

    # ==========================================================================
    # Categories view
    # ==========================================================================
    "Nuova Categoria": {"it": "Nuova Categoria", "en": "New Category", "es": "Nueva Categoría"},
    "Modifica Categoria": {"it": "Modifica Categoria", "en": "Edit Category", "es": "Editar Categoría"},

    # ==========================================================================
    # Locations view
    # ==========================================================================
    "Nuova Ubicazione": {"it": "Nuova Ubicazione", "en": "New Location", "es": "Nueva Ubicación"},
    "Modifica Ubicazione": {"it": "Modifica Ubicazione", "en": "Edit Location", "es": "Editar Ubicación"},
    "Stanza:": {"it": "Stanza:", "en": "Room:", "es": "Sala:"},

    # ==========================================================================
    # Conservations view
    # ==========================================================================
    "Nuova Conservazione": {"it": "Nuova Conservazione", "en": "New Storage Condition", "es": "Nueva Condición de Almacenamiento"},
    "Modifica Conservazione": {"it": "Modifica Conservazione", "en": "Edit Storage Condition", "es": "Editar Condición de Almacenamiento"},

    # ==========================================================================
    # Funding sources view
    # ==========================================================================
    "Nuova Fonte": {"it": "Nuova Fonte", "en": "New Funding Source", "es": "Nueva Fuente de Financiación"},
    "Modifica Fonte": {"it": "Modifica Fonte", "en": "Edit Funding Source", "es": "Editar Fuente de Financiación"},

    # ==========================================================================
    # Batch view
    # ==========================================================================
    "Modifica Lotto": {"it": "Modifica Lotto", "en": "Edit Batch", "es": "Editar Lote"},
    "Lotto:": {"it": "Lotto:", "en": "Batch:", "es": "Lote:"},
    "Scadenza:": {"it": "Scadenza:", "en": "Expiration:", "es": "Caducidad:"},
    "Il campo Lotto è obbligatorio!": {"it": "Il campo Lotto è obbligatorio!", "en": "Batch field is required!", "es": "¡El campo Lote es obligatorio!"},
    "Il campo Scadenza è obbligatorio!": {"it": "Il campo Scadenza è obbligatorio!", "en": "Expiration field is required!", "es": "¡El campo Caducidad es obligatorio!"},

    # ==========================================================================
    # Labels view
    # ==========================================================================
    "Carica etichette": {"it": "Carica etichette", "en": "Load labels", "es": "Cargar etiquetas"},
    "Quantità:": {"it": "Quantità:", "en": "Quantity:", "es": "Cantidad:"},
    "Numero etichette da creare:": {"it": "Numero etichette da creare:", "en": "Number of labels to create:", "es": "Número de etiquetas a crear:"},
    "Etichette create:": {"it": "Etichette create:", "en": "Labels created:", "es": "Etiquetas creadas:"},

    # ==========================================================================
    # Requests view
    # ==========================================================================
    "Riferimento": {"it": "Riferimento", "en": "Reference", "es": "Referencia"},
    "Data": {"it": "Data", "en": "Date", "es": "Fecha"},
    "Dettaglio Richiesta": {"it": "Dettaglio Richiesta", "en": "Request Details", "es": "Detalles de Solicitud"},
    "Aggiungi Articolo": {"it": "Aggiungi Articolo", "en": "Add Item", "es": "Agregar Artículo"},
    "Modifica Articolo": {"it": "Modifica Articolo", "en": "Edit Item", "es": "Editar Artículo"},
    "Elimina Articolo": {"it": "Elimina Articolo", "en": "Delete Item", "es": "Eliminar Artículo"},
    "Chiudi Richiesta": {"it": "Chiudi Richiesta", "en": "Close Request", "es": "Cerrar Solicitud"},
    "Elimina Richiesta": {"it": "Elimina Richiesta", "en": "Delete Request", "es": "Eliminar Solicitud"},
    "Aperte": {"it": "Aperte", "en": "Open", "es": "Abiertas"},
    "Chiuse": {"it": "Chiuse", "en": "Closed", "es": "Cerradas"},
    "Tutte": {"it": "Tutte", "en": "All", "es": "Todas"},
    "Generare una nuova richiesta?": {"it": "Generare una nuova richiesta?", "en": "Generate a new request?", "es": "¿Generar una nueva solicitud?"},
    "Nuova Richiesta": {"it": "Nuova Richiesta", "en": "New Request", "es": "Nueva Solicitud"},
    "Modifica Richiesta": {"it": "Modifica Richiesta", "en": "Edit Request", "es": "Editar Solicitud"},
    "Riferimento:": {"it": "Riferimento:", "en": "Reference:", "es": "Referencia:"},
    "Data:": {"it": "Data:", "en": "Date:", "es": "Fecha:"},
    "Articoli": {"it": "Articoli", "en": "Items", "es": "Artículos"},
    "Rimuovi Articolo": {"it": "Rimuovi Articolo", "en": "Remove Item", "es": "Quitar Artículo"},
    "Quantità": {"it": "Quantità", "en": "Quantity", "es": "Cantidad"},
    "Consegnato": {"it": "Consegnato", "en": "Delivered", "es": "Entregado"},

    # ==========================================================================
    # Delivery view
    # ==========================================================================
    "Nuova Consegna": {"it": "Nuova Consegna", "en": "New Delivery", "es": "Nueva Entrega"},
    "Registra Consegna": {"it": "Registra Consegna", "en": "Record Delivery", "es": "Registrar Entrega"},
    "Data consegna:": {"it": "Data consegna:", "en": "Delivery date:", "es": "Fecha de entrega:"},
    "Quantità consegnata:": {"it": "Quantità consegnata:", "en": "Quantity delivered:", "es": "Cantidad entregada:"},
    "Richieste aperte": {"it": "Richieste aperte", "en": "Open requests", "es": "Solicitudes abiertas"},
    "Seleziona richiesta": {"it": "Seleziona richiesta", "en": "Select request", "es": "Seleccionar solicitud"},

    # ==========================================================================
    # Stocks view
    # ==========================================================================
    "Tipo Stampa": {"it": "Tipo Stampa", "en": "Print Type", "es": "Tipo de Impresión"},
    "Stampa giacenze": {"it": "Stampa giacenze", "en": "Print stock", "es": "Imprimir existencias"},
    "Esporta": {"it": "Esporta", "en": "Export", "es": "Exportar"},

    # ==========================================================================
    # Expiring view
    # ==========================================================================
    "Lotti Scaduti": {"it": "Lotti Scaduti", "en": "Expired Batches", "es": "Lotes Caducados"},
    "Scadenze prossime": {"it": "Scadenze prossime", "en": "Upcoming expirations", "es": "Próximas caducidades"},
    "Giorni:": {"it": "Giorni:", "en": "Days:", "es": "Días:"},
    "Giorni alla scadenza": {"it": "Giorni alla scadenza", "en": "Days to expiration", "es": "Días hasta caducidad"},

    # ==========================================================================
    # Barcode view
    # ==========================================================================
    "Scarico etichette": {"it": "Scarico etichette", "en": "Unload labels", "es": "Descarga de etiquetas"},
    "Codice a barre:": {"it": "Codice a barre:", "en": "Barcode:", "es": "Código de barras:"},
    "Etichetta scaricata:": {"it": "Etichetta scaricata:", "en": "Label unloaded:", "es": "Etiqueta descargada:"},
    "Etichetta non trovata!": {"it": "Etichetta non trovata!", "en": "Label not found!", "es": "¡Etiqueta no encontrada!"},
    "Etichetta già scaricata!": {"it": "Etichetta già scaricata!", "en": "Label already unloaded!", "es": "¡Etiqueta ya descargada!"},

    # ==========================================================================
    # Custom label view
    # ==========================================================================
    "Righe da stampare": {"it": "Righe da stampare", "en": "Lines to print", "es": "Líneas a imprimir"},
    "Testo Etichetta": {"it": "Testo Etichetta", "en": "Label Text", "es": "Texto de Etiqueta"},
    "Includi nome laboratorio": {"it": "Includi nome laboratorio", "en": "Include laboratory name", "es": "Incluir nombre del laboratorio"},
    "Modelli Salvati": {"it": "Modelli Salvati", "en": "Saved Templates", "es": "Plantillas Guardadas"},
    "Etichetta personalizzata": {"it": "Etichetta personalizzata", "en": "Custom label", "es": "Etiqueta personalizada"},
    "Testo riga 1:": {"it": "Testo riga 1:", "en": "Text line 1:", "es": "Texto línea 1:"},
    "Testo riga 2:": {"it": "Testo riga 2:", "en": "Text line 2:", "es": "Texto línea 2:"},
    "Testo riga 3:": {"it": "Testo riga 3:", "en": "Text line 3:", "es": "Texto línea 3:"},
    "Codice barcode:": {"it": "Codice barcode:", "en": "Barcode code:", "es": "Código de barras:"},

    # ==========================================================================
    # Statistics views
    # ==========================================================================
    "Periodo di Analisi": {"it": "Periodo di Analisi", "en": "Analysis Period", "es": "Período de Análisis"},
    "Riepilogo": {"it": "Riepilogo", "en": "Summary", "es": "Resumen"},
    "Analisi Scadenze": {"it": "Analisi Scadenze", "en": "Expiration Analysis", "es": "Análisis de Caducidades"},
    "Analisi Storica Scaduti": {"it": "Analisi Storica Scaduti", "en": "Historical Expired Analysis", "es": "Análisis Histórico de Caducados"},
    "Periodo scadenza - Da:": {"it": "Periodo scadenza - Da:", "en": "Expiration period - From:", "es": "Período de caducidad - Desde:"},
    "Anno scorso": {"it": "Anno scorso", "en": "Last year", "es": "Año pasado"},
    "6 mesi fa": {"it": "6 mesi fa", "en": "6 months ago", "es": "Hace 6 meses"},
    "Oggi": {"it": "Oggi", "en": "Today", "es": "Hoy"},
    "+30 gg": {"it": "+30 gg", "en": "+30 days", "es": "+30 días"},
    "+90 gg": {"it": "+90 gg", "en": "+90 days", "es": "+90 días"},
    "30 gg": {"it": "30 gg", "en": "30 days", "es": "30 días"},
    "90 gg": {"it": "90 gg", "en": "90 days", "es": "90 días"},
    "6 mesi": {"it": "6 mesi", "en": "6 months", "es": "6 meses"},
    "Anno": {"it": "Anno", "en": "Year", "es": "Año"},
    "Lotti Scaduti (con giacenza residua)": {"it": "Lotti Scaduti (con giacenza residua)", "en": "Expired Batches (with remaining stock)", "es": "Lotes Caducados (con existencias restantes)"},
    "Efficienza FEFO (First Expired First Out)": {"it": "Efficienza FEFO (First Expired First Out)", "en": "FEFO Efficiency (First Expired First Out)", "es": "Eficiencia FEFO (Primero en Caducar, Primero en Salir)"},
    "Residuo": {"it": "Residuo", "en": "Remaining", "es": "Restante"},
    "Usato": {"it": "Usato", "en": "Used", "es": "Usado"},
    "Perdita %": {"it": "Perdita %", "en": "Loss %", "es": "Pérdida %"},
    "Etichette Scaricate": {"it": "Etichette Scaricate", "en": "Unloaded Labels", "es": "Etiquetas Descargadas"},
    "FEFO Corrette": {"it": "FEFO Corrette", "en": "FEFO Correct", "es": "FEFO Correctas"},
    "Efficienza %": {"it": "Efficienza %", "en": "Efficiency %", "es": "Eficiencia %"},
    "Lotti scaduti con giacenza:": {"it": "Lotti scaduti con giacenza:", "en": "Expired batches with stock:", "es": "Lotes caducados con existencias:"},
    "Etichette scadute (perdite):": {"it": "Etichette scadute (perdite):", "en": "Expired labels (losses):", "es": "Etiquetas caducadas (pérdidas):"},
    "In scadenza (30 gg):": {"it": "In scadenza (30 gg):", "en": "Expiring (30 days):", "es": "Por caducar (30 días):"},
    "Analisi Fornitori": {"it": "Analisi Fornitori", "en": "Supplier Analysis", "es": "Análisis de Proveedores"},
    "Ordini": {"it": "Ordini", "en": "Orders", "es": "Pedidos"},
    "Ordinato": {"it": "Ordinato", "en": "Ordered", "es": "Pedido"},
    "Completamento %": {"it": "Completamento %", "en": "Completion %", "es": "Completado %"},
    "TAT medio (gg)": {"it": "TAT medio (gg)", "en": "Avg TAT (days)", "es": "TAT promedio (días)"},
    "Analisi Tempi (TAT)": {"it": "Analisi Tempi (TAT)", "en": "Time Analysis (TAT)", "es": "Análisis de Tiempos (TAT)"},
    "Metriche TAT": {"it": "Metriche TAT", "en": "TAT Metrics", "es": "Métricas TAT"},
    "Tempo Richiesta → Consegna (per fornitore)": {"it": "Tempo Richiesta → Consegna (per fornitore)", "en": "Request → Delivery Time (by supplier)", "es": "Tiempo Solicitud → Entrega (por proveedor)"},
    "Tempo in Magazzino (Carico → Scarico)": {"it": "Tempo in Magazzino (Carico → Scarico)", "en": "Warehouse Time (Load → Unload)", "es": "Tiempo en Almacén (Carga → Descarga)"},
    "Media (gg)": {"it": "Media (gg)", "en": "Avg (days)", "es": "Promedio (días)"},
    "Min (gg)": {"it": "Min (gg)", "en": "Min (days)", "es": "Mín (días)"},
    "Max (gg)": {"it": "Max (gg)", "en": "Max (days)", "es": "Máx (días)"},
    "TAT medio ordini:": {"it": "TAT medio ordini:", "en": "Avg order TAT:", "es": "TAT promedio pedidos:"},
    "TAT medio magazzino:": {"it": "TAT medio magazzino:", "en": "Avg warehouse TAT:", "es": "TAT promedio almacén:"},
    "giorni": {"it": "giorni", "en": "days", "es": "días"},
    "Analisi Consumi": {"it": "Analisi Consumi", "en": "Consumption Analysis", "es": "Análisis de Consumos"},
    "Consumi per Prodotto": {"it": "Consumi per Prodotto", "en": "Consumption by Product", "es": "Consumos por Producto"},
    "Consumi per Categoria": {"it": "Consumi per Categoria", "en": "Consumption by Category", "es": "Consumos por Categoría"},
    "Analisi Rotazione": {"it": "Analisi Rotazione", "en": "Rotation Analysis", "es": "Análisis de Rotación"},
    "Analisi Rotazione e ABC": {"it": "Analisi Rotazione e ABC", "en": "Rotation and ABC Analysis", "es": "Análisis de Rotación y ABC"},
    "Dashboard Statistiche": {"it": "Dashboard Statistiche", "en": "Statistics Dashboard", "es": "Panel de Estadísticas"},
    "Dashboard Magazzino": {"it": "Dashboard Magazzino", "en": "Warehouse Dashboard", "es": "Panel de Almacén"},
    "Sotto Soglia Riordino": {"it": "Sotto Soglia Riordino", "en": "Below Reorder Threshold", "es": "Bajo Umbral de Reorden"},
    "Movimenti (ultimi 30 giorni)": {"it": "Movimenti (ultimi 30 giorni)", "en": "Movements (last 30 days)", "es": "Movimientos (últimos 30 días)"},
    "Top 5 Consumi (30 giorni)": {"it": "Top 5 Consumi (30 giorni)", "en": "Top 5 Consumption (30 days)", "es": "Top 5 Consumos (30 días)"},
    "Prodotti attivi:": {"it": "Prodotti attivi:", "en": "Active products:", "es": "Productos activos:"},
    "Etichette in giacenza:": {"it": "Etichette in giacenza:", "en": "Labels in stock:", "es": "Etiquetas en existencia:"},
    "Lotti attivi:": {"it": "Lotti attivi:", "en": "Active batches:", "es": "Lotes activos:"},
    "Prodotti sotto soglia:": {"it": "Prodotti sotto soglia:", "en": "Products below threshold:", "es": "Productos bajo umbral:"},
    "Prodotti esauriti:": {"it": "Prodotti esauriti:", "en": "Out of stock products:", "es": "Productos agotados:"},
    "Lotti scaduti:": {"it": "Lotti scaduti:", "en": "Expired batches:", "es": "Lotes caducados:"},
    "In scadenza (60 gg):": {"it": "In scadenza (60 gg):", "en": "Expiring (60 days):", "es": "Por caducar (60 días):"},
    "In scadenza (90 gg):": {"it": "In scadenza (90 gg):", "en": "Expiring (90 days):", "es": "Por caducar (90 días):"},
    "Etichette caricate:": {"it": "Etichette caricate:", "en": "Labels loaded:", "es": "Etiquetas cargadas:"},
    "Etichette scaricate:": {"it": "Etichette scaricate:", "en": "Labels unloaded:", "es": "Etiquetas descargadas:"},
    "Etichette annullate:": {"it": "Etichette annullate:", "en": "Labels cancelled:", "es": "Etiquetas canceladas:"},
    "Richieste aperte:": {"it": "Richieste aperte:", "en": "Open requests:", "es": "Solicitudes abiertas:"},
    "Articoli in attesa:": {"it": "Articoli in attesa:", "en": "Pending items:", "es": "Artículos pendientes:"},
    "Nessun dato disponibile": {"it": "Nessun dato disponibile", "en": "No data available", "es": "Sin datos disponibles"},
    "Giacenza": {"it": "Giacenza", "en": "Stock", "es": "Existencias"},
    "Consumato": {"it": "Consumato", "en": "Consumed", "es": "Consumido"},
    "Filtri": {"it": "Filtri", "en": "Filters", "es": "Filtros"},
    "Media/Mese": {"it": "Media/Mese", "en": "Avg/Month", "es": "Prom/Mes"},
    "Totale prodotti": {"it": "Totale prodotti", "en": "Total products", "es": "Total productos"},
    "Totale consumato": {"it": "Totale consumato", "en": "Total consumed", "es": "Total consumido"},
    "Periodo": {"it": "Periodo", "en": "Period", "es": "Período"},
    "Esporta Consumi": {"it": "Esporta Consumi", "en": "Export Consumption", "es": "Exportar Consumos"},
    "60 gg": {"it": "60 gg", "en": "60 days", "es": "60 días"},
    "Classificazione ABC": {"it": "Classificazione ABC", "en": "ABC Classification", "es": "Clasificación ABC"},
    "Classificazione ABC:": {"it": "Classificazione ABC:", "en": "ABC Classification:", "es": "Clasificación ABC:"},
    "A = Alta rotazione (80% movimenti)": {"it": "A = Alta rotazione (80% movimenti)", "en": "A = High rotation (80% movements)", "es": "A = Alta rotación (80% movimientos)"},
    "B = Media rotazione": {"it": "B = Media rotazione", "en": "B = Medium rotation", "es": "B = Media rotación"},
    "C = Bassa rotazione": {"it": "C = Bassa rotazione", "en": "C = Low rotation", "es": "C = Baja rotación"},
    "Copertura (gg)": {"it": "Copertura (gg)", "en": "Coverage (days)", "es": "Cobertura (días)"},
    "ABC": {"it": "ABC", "en": "ABC", "es": "ABC"},
    "Classe A": {"it": "Classe A", "en": "Class A", "es": "Clase A"},
    "Classe B": {"it": "Classe B", "en": "Class B", "es": "Clase B"},
    "Classe C": {"it": "Classe C", "en": "Class C", "es": "Clase C"},
    "Esporta Rotazione": {"it": "Esporta Rotazione", "en": "Export Rotation", "es": "Exportar Rotación"},
    "Classe": {"it": "Classe", "en": "Class", "es": "Clase"},
    "% Cumulativa": {"it": "% Cumulativa", "en": "Cumulative %", "es": "% Acumulado"},

    # ==========================================================================
    # Package history view
    # ==========================================================================
    "Storico Ordini": {"it": "Storico Ordini", "en": "Order History", "es": "Historial de Pedidos"},
    "Richiesta": {"it": "Richiesta", "en": "Request", "es": "Solicitud"},
    "Data Richiesta": {"it": "Data Richiesta", "en": "Request Date", "es": "Fecha de Solicitud"},
    "Qty Ordinata": {"it": "Qty Ordinata", "en": "Qty Ordered", "es": "Cant. Pedida"},
    "Qty Consegnata": {"it": "Qty Consegnata", "en": "Qty Delivered", "es": "Cant. Entregada"},
    "Data Consegna": {"it": "Data Consegna", "en": "Delivery Date", "es": "Fecha de Entrega"},

    # ==========================================================================
    # Messages
    # ==========================================================================
    "Vuoi salvare?": {"it": "Vuoi salvare?", "en": "Do you want to save?", "es": "¿Desea guardar?"},
    "Operazione annullata.": {"it": "Operazione annullata.", "en": "Operation cancelled.", "es": "Operación cancelada."},
    "Seleziona un elemento!": {"it": "Seleziona un elemento!", "en": "Select an item!", "es": "¡Seleccione un elemento!"},
    "Confermi eliminazione?": {"it": "Confermi eliminazione?", "en": "Confirm deletion?", "es": "¿Confirma eliminación?"},
    "Riavvio richiesto": {"it": "È necessario riavviare l'applicazione per applicare la nuova lingua.\n\nRiavviare ora?", "en": "Application restart is required to apply the new language.\n\nRestart now?", "es": "Es necesario reiniciar la aplicación para aplicar el nuevo idioma.\n\n¿Reiniciar ahora?"},
    "Lingua cambiata": {"it": "Lingua cambiata", "en": "Language changed", "es": "Idioma cambiado"},
    "Le date non sono valide!": {"it": "Le date non sono valide!", "en": "Dates are not valid!", "es": "¡Las fechas no son válidas!"},
    "Nessun dato nel periodo selezionato": {"it": "Nessun dato nel periodo selezionato", "en": "No data in selected period", "es": "Sin datos en el período seleccionado"},
    "esiste già!": {"it": "esiste già!", "en": "already exists!", "es": "¡ya existe!"},
    "è già assegnato!": {"it": "è già assegnato!", "en": "is already assigned!", "es": "¡ya está asignado!"},
    "Sì": {"it": "Sì", "en": "Yes", "es": "Sí"},
    "No": {"it": "No", "en": "No", "es": "No"},

    # ==========================================================================
    # Menu - Purchases
    # ==========================================================================
    "Acquisti": {"it": "Acquisti", "en": "Purchases", "es": "Compras"},
    "Delibere": {"it": "Delibere", "en": "Deliberations", "es": "Deliberaciones"},
    "Listino Prezzi": {"it": "Listino Prezzi", "en": "Price List", "es": "Lista de Precios"},
    "Fonti Package": {"it": "Fonti Package", "en": "Package Sources", "es": "Fuentes de Paquetes"},
    "Fonti Finanziamento Packages": {"it": "Fonti Finanziamento Packages", "en": "Package Funding Sources", "es": "Fuentes de Financiación de Paquetes"},

    # ==========================================================================
    # Deliberations view
    # ==========================================================================
    "Nuova Delibera": {"it": "Nuova Delibera", "en": "New Deliberation", "es": "Nueva Deliberación"},
    "Modifica Delibera": {"it": "Modifica Delibera", "en": "Edit Deliberation", "es": "Editar Deliberación"},
    "Numero:": {"it": "Numero:", "en": "Number:", "es": "Número:"},
    "Importo:": {"it": "Importo:", "en": "Amount:", "es": "Importe:"},
    "CIG:": {"it": "CIG:", "en": "CIG:", "es": "CIG:"},
    "Attiva:": {"it": "Attiva:", "en": "Active:", "es": "Activa:"},
    "Il campo Numero è obbligatorio!": {"it": "Il campo Numero è obbligatorio!", "en": "Number field is required!", "es": "¡El campo Número es obligatorio!"},
    "Importo": {"it": "Importo", "en": "Amount", "es": "Importe"},
    "CIG": {"it": "CIG", "en": "CIG", "es": "CIG"},
    "Delibera": {"it": "Delibera", "en": "Deliberation", "es": "Deliberación"},
    "Attive": {"it": "Attive", "en": "Active", "es": "Activas"},
    "Numero": {"it": "Numero", "en": "Number", "es": "Número"},

    # ==========================================================================
    # Prices view
    # ==========================================================================
    "Nuovo Prezzo": {"it": "Nuovo Prezzo", "en": "New Price", "es": "Nuevo Precio"},
    "Modifica Prezzo": {"it": "Modifica Prezzo", "en": "Edit Price", "es": "Editar Precio"},
    "Prezzo:": {"it": "Prezzo:", "en": "Price:", "es": "Precio:"},
    "Prezzo": {"it": "Prezzo", "en": "Price", "es": "Precio"},
    "IVA %:": {"it": "IVA %:", "en": "VAT %:", "es": "IVA %:"},
    "IVA %": {"it": "IVA %", "en": "VAT %", "es": "IVA %"},
    "Valido dal:": {"it": "Valido dal:", "en": "Valid from:", "es": "Válido desde:"},
    "Valido dal": {"it": "Valido dal", "en": "Valid from", "es": "Válido desde"},
    "Il campo Prezzo è obbligatorio!": {"it": "Il campo Prezzo è obbligatorio!", "en": "Price field is required!", "es": "¡El campo Precio es obligatorio!"},
    "Il campo Valido dal è obbligatorio!": {"it": "Il campo Valido dal è obbligatorio!", "en": "Valid from field is required!", "es": "¡El campo Válido desde es obligatorio!"},

    # ==========================================================================
    # Package fundings view
    # ==========================================================================
    "Nuova Fonte Finanziamento": {"it": "Nuova Fonte Finanziamento", "en": "New Funding Source", "es": "Nueva Fuente de Financiación"},
    "Modifica Fonte Finanziamento": {"it": "Modifica Fonte Finanziamento", "en": "Edit Funding Source", "es": "Editar Fuente de Financiación"},
    "Prodotto:": {"it": "Prodotto:", "en": "Product:", "es": "Producto:"},
    "Package:": {"it": "Package:", "en": "Package:", "es": "Paquete:"},
    "Fonte Finanziamento:": {"it": "Fonte Finanziamento:", "en": "Funding Source:", "es": "Fuente de Financiación:"},
    "Selezionare un Package!": {"it": "Selezionare un Package!", "en": "Select a Package!", "es": "¡Seleccione un Paquete!"},
    "Selezionare una Fonte Finanziamento!": {"it": "Selezionare una Fonte Finanziamento!", "en": "Select a Funding Source!", "es": "¡Seleccione una Fuente de Financiación!"},
    "Legenda": {"it": "Legenda", "en": "Legend", "es": "Leyenda"},
    "In Gara": {"it": "In Gara", "en": "In Tender", "es": "En Licitación"},
    "Economia": {"it": "Economia", "en": "Direct Purchase", "es": "Compra Directa"},
    "(opzionale - se in gara)": {"it": "(opzionale - se in gara)", "en": "(optional - if in tender)", "es": "(opcional - si en licitación)"},
    "Fonti/Delibere": {"it": "Fonti/Delibere", "en": "Sources/Delib.", "es": "Fuentes/Delib."},
    "Cerca Package:": {"it": "Cerca Package:", "en": "Search Package:", "es": "Buscar Paquete:"},
    "(descrizione o codice)": {"it": "(descrizione o codice)", "en": "(description or code)", "es": "(descripción o código)"},
    "Risultati:": {"it": "Risultati:", "en": "Results:", "es": "Resultados:"},
    "Selezionato:": {"it": "Selezionato:", "en": "Selected:", "es": "Seleccionado:"},

    # ==========================================================================
    # Report Fundings
    # ==========================================================================
    "Report Fonti": {"it": "Report Fonti", "en": "Funding Report", "es": "Informe de Fuentes"},
    "Report Fonti Finanziamento": {"it": "Report Fonti Finanziamento", "en": "Funding Sources Report", "es": "Informe de Fuentes de Financiación"},
    "Nessun dato da esportare!": {"it": "Nessun dato da esportare!", "en": "No data to export!", "es": "¡No hay datos para exportar!"},
    "File esportato": {"it": "File esportato", "en": "File exported", "es": "Archivo exportado"},
    "Errore durante l'esportazione": {"it": "Errore durante l'esportazione", "en": "Error during export", "es": "Error durante la exportación"},
    "Errore durante esportazione": {"it": "Errore durante esportazione", "en": "Error during export", "es": "Error durante la exportación"},

    # ==========================================================================
    # Settings
    # ==========================================================================
    "Impostazioni Laboratorio": {"it": "Impostazioni Laboratorio", "en": "Laboratory Settings", "es": "Configuración del Laboratorio"},
    "Ospedale:": {"it": "Ospedale:", "en": "Hospital:", "es": "Hospital:"},
    "Laboratorio:": {"it": "Laboratorio:", "en": "Laboratory:", "es": "Laboratorio:"},
    "Responsabile:": {"it": "Responsabile:", "en": "Manager:", "es": "Responsable:"},
    "Stanza/Locale:": {"it": "Stanza/Locale:", "en": "Room/Location:", "es": "Sala/Local:"},
    "Telefono:": {"it": "Telefono:", "en": "Phone:", "es": "Teléfono:"},
    "IVA predefinita %:": {"it": "IVA predefinita %:", "en": "Default VAT %:", "es": "IVA predeterminado %:"},
    "Timeout inattività (min):": {"it": "Timeout inattività (min):", "en": "Idle timeout (min):", "es": "Tiempo de espera inactivo (min):"},
    "(0 = disabilitato)": {"it": "(0 = disabilitato)", "en": "(0 = disabled)", "es": "(0 = deshabilitado)"},
    "Impostazioni salvate.": {"it": "Impostazioni salvate.", "en": "Settings saved.", "es": "Configuración guardada."},
}


class I18N:
    """Internationalization helper class."""

    def __init__(self, language=None):
        """
        Initialize with specified language.

        Args:
            language: Language code ('it', 'en' or 'es'). Defaults to DEFAULT_LANGUAGE.
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
            language: Language code ('it', 'en' or 'es')
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
