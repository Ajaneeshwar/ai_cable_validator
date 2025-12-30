/**
 * API Types for Cable Design Validation
 */

export type ValidationStatus = 'PASS' | 'WARN' | 'FAIL';

export interface CableDesignInput {
    standard?: string;
    voltage?: string;
    conductor_material?: string;
    conductor_class?: string;
    csa?: number;
    insulation_material?: string;
    insulation_thickness?: number;
}

export interface ValidationRequest {
    design?: CableDesignInput;
    free_text?: string;
    design_id?: number;
}

export interface FieldValidation {
    field: string;
    provided?: string;
    expected?: string;
    status: ValidationStatus;
    comment: string;
}

export interface ConfidenceScore {
    overall: number;
    reasoning?: string;
}

export interface ExtractedFields {
    standard?: string;
    voltage?: string;
    conductor_material?: string;
    conductor_class?: string;
    csa?: number;
    insulation_material?: string;
    insulation_thickness?: number;
}

export interface ValidationResult {
    fields: ExtractedFields;
    validation: FieldValidation[];
    confidence: ConfidenceScore;
    reasoning: string;
}

export interface ValidationResponse {
    success: boolean;
    message: string;
    data?: ValidationResult;
    input_type: string;
}

export interface CableDesign {
    id: number;
    name: string;
    standard?: string;
    voltage?: string;
    conductor_material?: string;
    conductor_class?: string;
    csa?: number;
    insulation_material?: string;
    insulation_thickness?: number;
    created_at?: string;
}

export interface DesignListResponse {
    success: boolean;
    data: CableDesign[];
    count: number;
}
