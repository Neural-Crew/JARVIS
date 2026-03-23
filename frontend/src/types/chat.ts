export interface ToolCall {
  id: string;
  name: string;
  status: "running" | "success" | "error";
  input?: string;
  output?: string;
  error?: string;
  payload?: ToolPayload;
}

export interface ChartPoint {
  timestamp: string;
  [key: string]: string | number;
}

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

export interface ToolPayload {
  type: "chart";
  chart: ChartSpec;
}

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
  toolCalls?: ToolCall[];
}

export interface Conversation {
  id: string;
  title: string;
  messages: Message[];
  createdAt: Date;
  updatedAt: Date;
}
