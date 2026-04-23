/**
 * Représente un appel d'outil (tool call) par l'agent.
 * @typedef {Object} ToolCall
 * @property {string} id - Identifiant unique de l'appel.
 * @property {string} name - Nom de l'outil appelé.
 * @property {"running" | "success" | "error"} status - État actuel de l'appel.
 * @property {string} [input] - Entrée brute envoyée à l'outil.
 * @property {string} [output] - Sortie brute renvoyée par l'outil.
 * @property {string} [error] - Message d'erreur si l'appel a échoué.
 * @property {ToolPayload} [payload] - Données structurées extraites de la sortie.
 */
export interface ToolCall {
  id: string;
  name: string;
  status: "running" | "success" | "error";
  input?: string;
  output?: string;
  error?: string;
  payload?: ToolPayload;
}

/**
 * Représente un point de données dans un graphique.
 * @typedef {Object} ChartPoint
 * @property {string} timestamp - Horodatage du point.
 * @property {string | number} [key] - Valeur mesurée pour une clé donnée.
 */
export interface ChartPoint {
  timestamp: string;
  [key: string]: string | number;
}

/**
 * Spécification complète pour le rendu d'un graphique côté frontend.
 * @typedef {Object} ChartSpec
 * @property {"chart_spec"} kind - Discriminateur de type.
 * @property {"line"} chart_type - Type de graphique (actuellement uniquement 'line').
 * @property {string} title - Titre du graphique.
 * @property {string} x_key - Clé utilisée pour l'axe X (temps).
 * @property {string[]} y_keys - Liste des clés à tracer sur l'axe Y.
 * @property {ChartPoint[]} points - Liste des points de données.
 * @property {string} [unit] - Unité de mesure.
 * @property {Object} [metadata] - Métadonnées supplémentaires.
 */
export interface ChartSpec {
  kind: "chart_spec";
  chart_type: "line";
  title: string;
  x_key: string;
  y_keys: string[];
  points: ChartPoint[];
  unit?: string;
  metadata?: {
    sensor_type?: string;
    device_id?: string;
    aggregation?: "raw" | "hour" | "day";
    record_count?: number;
    source?: string;
  };
}

/**
 * Payload structuré pour les outils renvoyant des données riches.
 * @typedef {Object} ToolPayload
 * @property {"chart"} type - Type de payload.
 * @property {ChartSpec} chart - Spécification du graphique.
 */
export interface ToolPayload {
  type: "chart";
  chart: ChartSpec;
}

/**
 * Représente un message dans une conversation.
 * @typedef {Object} Message
 * @property {string} id - Identifiant unique du message.
 * @property {"user" | "assistant"} role - Rôle de l'émetteur.
 * @property {string} content - Contenu textuel du message.
 * @property {Date} timestamp - Date d'émission.
 * @property {ToolCall[]} [toolCalls] - Liste des appels d'outils associés.
 */
export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
  toolCalls?: ToolCall[];
}

/**
 * Représente une session de discussion complète.
 * @typedef {Object} Conversation
 * @property {string} id - Identifiant unique de la discussion.
 * @property {string} title - Titre de la discussion.
 * @property {Message[]} messages - Historique des messages.
 * @property {Date} createdAt - Date de création.
 * @property {Date} updatedAt - Date de dernière mise à jour.
 */
export interface Conversation {
  id: string;
  title: string;
  messages: Message[];
  createdAt: Date;
  updatedAt: Date;
}
