/**
 * Design Validator Page
 * 
 * Main page for AI-driven cable design validation
 */
'use client';

import { useState, useEffect } from 'react';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import Alert from '@mui/material/Alert';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import Snackbar from '@mui/material/Snackbar';
import ElectricalServicesIcon from '@mui/icons-material/ElectricalServices';
import MenuBookIcon from '@mui/icons-material/MenuBook';
import { InputPanel, ResultsTable, ReasoningDrawer } from '@/components';
import { validateDesign, getDesignList } from '@/services/api';
import {
    CableDesignInput,
    CableDesign,
    ValidationResult,
    FieldValidation
} from '@/types/validation';

export default function DesignValidatorPage() {
    const [isLoading, setIsLoading] = useState(false);
    const [savedDesigns, setSavedDesigns] = useState<CableDesign[]>([]);
    const [validationResult, setValidationResult] = useState<ValidationResult | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [drawerOpen, setDrawerOpen] = useState(false);
    const [snackbarOpen, setSnackbarOpen] = useState(false);

    // Load saved designs on mount
    useEffect(() => {
        loadSavedDesigns();
    }, []);

    const loadSavedDesigns = async () => {
        try {
            const response = await getDesignList();
            if (response.success) {
                setSavedDesigns(response.data);
            }
        } catch (err) {
            console.error('Failed to load saved designs:', err);
        }
    };

    const handleValidate = async (
        design?: CableDesignInput,
        freeText?: string,
        designId?: number
    ) => {
        setIsLoading(true);
        setError(null);

        try {
            const response = await validateDesign({
                design,
                free_text: freeText,
                design_id: designId,
            });

            if (response.success && response.data) {
                setValidationResult(response.data);
                setDrawerOpen(true);
                setSnackbarOpen(true);
            } else {
                setError(response.message || 'Validation failed');
            }
        } catch (err: any) {
            console.error('Validation error:', err);
            setError(
                err.response?.data?.detail ||
                err.message ||
                'Failed to validate design. Please check if the backend is running.'
            );
        } finally {
            setIsLoading(false);
        }
    };

    const validations: FieldValidation[] = validationResult?.validation || [];

    return (
        <Box
            sx={{
                minHeight: '100vh',
                background: 'linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%)',
                py: 4,
            }}
        >
            <Container maxWidth="xl">
                {/* Header */}
                <Box
                    sx={{
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                        mb: 4,
                    }}
                >
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <Box
                            sx={{
                                width: 56,
                                height: 56,
                                borderRadius: 2,
                                background: 'linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                mr: 2,
                            }}
                        >
                            <ElectricalServicesIcon sx={{ fontSize: 32, color: 'white' }} />
                        </Box>
                        <Box>
                            <Typography variant="h4" fontWeight={700}>
                                Cable Design Validator
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                                AI-powered IEC 60502-1 & IEC 60228 compliance validation
                            </Typography>
                        </Box>
                    </Box>

                    <Button
                        variant="outlined"
                        startIcon={<MenuBookIcon />}
                        onClick={() => setDrawerOpen(true)}
                        disabled={!validationResult}
                    >
                        View AI Reasoning
                    </Button>
                </Box>

                {/* Error Alert */}
                {error && (
                    <Alert
                        severity="error"
                        onClose={() => setError(null)}
                        sx={{ mb: 3 }}
                    >
                        {error}
                    </Alert>
                )}

                {/* Main Content */}
                <Grid container spacing={3}>
                    <Grid item xs={12} md={5}>
                        <InputPanel
                            onValidate={handleValidate}
                            isLoading={isLoading}
                            savedDesigns={savedDesigns}
                        />
                    </Grid>

                    <Grid item xs={12} md={7}>
                        <ResultsTable
                            validations={validations}
                            onRowClick={() => setDrawerOpen(true)}
                        />
                    </Grid>
                </Grid>

                {/* Confidence Summary Card */}
                {validationResult && (
                    <Box
                        sx={{
                            mt: 3,
                            p: 3,
                            borderRadius: 3,
                            background: 'linear-gradient(135deg, rgba(59, 130, 246, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%)',
                            border: '1px solid rgba(255,255,255,0.1)',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'space-between',
                        }}
                    >
                        <Box>
                            <Typography variant="body2" color="text.secondary">
                                Overall Confidence Score
                            </Typography>
                            <Typography variant="h4" fontWeight={700}>
                                {Math.round(validationResult.confidence.overall * 100)}%
                            </Typography>
                        </Box>

                        <Box sx={{ textAlign: 'right' }}>
                            <Typography variant="body2" color="text.secondary">
                                Validation Summary
                            </Typography>
                            <Box sx={{ display: 'flex', gap: 2 }}>
                                <Typography color="success.main" fontWeight={600}>
                                    {validations.filter(v => v.status === 'PASS').length} PASS
                                </Typography>
                                <Typography color="warning.main" fontWeight={600}>
                                    {validations.filter(v => v.status === 'WARN').length} WARN
                                </Typography>
                                <Typography color="error.main" fontWeight={600}>
                                    {validations.filter(v => v.status === 'FAIL').length} FAIL
                                </Typography>
                            </Box>
                        </Box>
                    </Box>
                )}

                {/* AI Reasoning Drawer */}
                <ReasoningDrawer
                    open={drawerOpen}
                    onClose={() => setDrawerOpen(false)}
                    result={validationResult}
                />

                {/* Success Snackbar */}
                <Snackbar
                    open={snackbarOpen}
                    autoHideDuration={4000}
                    onClose={() => setSnackbarOpen(false)}
                    message="Validation completed successfully"
                />
            </Container>
        </Box>
    );
}
