export type User = {
  id: string;
  name: string;
  email: string;
  total_analyses: number;
  created_at: string;
  updated_at: string;
};

export type LipRGB = {
  r: number;
  g: number;
  b: number;
};

export type LipType = "Pinkish" | "Brownish" | "Dark";

export type Recommendation = {
  shade_name: string;
  category: string;
  score: number;
  rgb: LipRGB;
};

export type Analysis = {
  id: string;
  user_id: string;
  original_image_url: string;
  cropped_lip_image_url: string;
  rgb: LipRGB;
  lip_type: LipType;
  confidence: number;
  recommendations: Recommendation[];
  status: "completed" | "failed";
  created_at: string;
};

export type Lipstick = {
  id: string;
  shade_name: string;
  category: string;
  rgb: LipRGB;
  lip_type_tag: LipType;
  metadata?: Record<string, unknown>;
};
