export interface LipRGB {
  r: number;
  g: number;
  b: number;
}

export interface Recommendation {
  shade_name: string;
  category: string;
  score: number;
  rgb: LipRGB;
}

export interface AnalysisResult {
  id: string;
  user_id: string;
  original_image_url: string;
  cropped_lip_image_url: string;
  brushed_lip_image_url?: string | null;
  rgb: LipRGB;
  lip_type: string;
  confidence: number;
  recommendations: Recommendation[];
  status: string;
  created_at: string;
}
