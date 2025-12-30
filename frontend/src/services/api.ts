/**
 * API Service for Cable Design Validation
 */
import axios from 'axios';
import {
    ValidationRequest,
    ValidationResponse,
    DesignListResponse
} from '@/types/validation';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

/**
 * Validate a cable design against IEC standards
 */
export async function validateDesign(request: ValidationRequest): Promise<ValidationResponse> {
    const response = await apiClient.post<ValidationResponse>('/design/validate', request);
    return response.data;
}

/**
 * Get all cable designs from the database
 */
export async function getDesignList(): Promise<DesignListResponse> {
    const response = await apiClient.get<DesignListResponse>('/design/list');
    return response.data;
}

/**
 * Get a specific cable design by ID
 */
export async function getDesignById(id: number) {
    const response = await apiClient.get(`/design/${id}`);
    return response.data;
}
