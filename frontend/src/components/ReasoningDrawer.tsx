/**
 * AI Reasoning Drawer Component
 * 
 * Side drawer displaying AI reasoning and confidence score
 */
'use client';

import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import Divider from '@mui/material/Divider';
import LinearProgress from '@mui/material/LinearProgress';
import Chip from '@mui/material/Chip';
import CloseIcon from '@mui/icons-material/Close';
import PsychologyIcon from '@mui/icons-material/Psychology';
import SpeedIcon from '@mui/icons-material/Speed';
import InfoIcon from '@mui/icons-material/Info';
import { ValidationResult } from '@/types/validation';

interface ReasoningDrawerProps {
    open: boolean;
    onClose: () => void;
    result: ValidationResult | null;
}

function getConfidenceColor(score: number): 'success' | 'warning' | 'error' {
    if (score >= 0.85) return 'success';
    if (score >= 0.65) return 'warning';
    return 'error';
}

function getConfidenceLabel(score: number): string {
    if (score >= 0.85) return 'High Confidence';
    if (score >= 0.65) return 'Medium Confidence';
    return 'Low Confidence';
}

export default function ReasoningDrawer({ open, onClose, result }: ReasoningDrawerProps) {
    if (!result) return null;

    const confidence = result.confidence.overall;
    const confidencePercent = Math.round(confidence * 100);
    const confidenceColor = getConfidenceColor(confidence);

    return (
        <Drawer
            anchor="right"
            open={open}
            onClose={onClose}
            sx={{
                '& .MuiDrawer-paper': {
                    width: { xs: '100%', sm: 450 },
                    background: 'linear-gradient(180deg, #1e293b 0%, #0f172a 100%)',
                    borderLeft: '1px solid rgba(255,255,255,0.1)',
                },
            }}
        >
            <Box sx={{ p: 3 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 3 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <PsychologyIcon sx={{ fontSize: 28, mr: 1, color: 'primary.main' }} />
                        <Typography variant="h6" fontWeight={700}>
                            AI Analysis
                        </Typography>
                    </Box>
                    <IconButton onClick={onClose} size="small">
                        <CloseIcon />
                    </IconButton>
                </Box>

                {/* Confidence Score */}
                <Box
                    sx={{
                        p: 3,
                        borderRadius: 2,
                        background: 'rgba(59, 130, 246, 0.1)',
                        border: '1px solid rgba(59, 130, 246, 0.2)',
                        mb: 3,
                    }}
                >
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                        <SpeedIcon sx={{ mr: 1, color: 'primary.main' }} />
                        <Typography variant="subtitle1" fontWeight={600}>
                            Confidence Score
                        </Typography>
                    </Box>

                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                        <Typography variant="h3" fontWeight={700} sx={{ mr: 2 }}>
                            {confidencePercent}%
                        </Typography>
                        <Chip
                            label={getConfidenceLabel(confidence)}
                            color={confidenceColor}
                            size="small"
                        />
                    </Box>

                    <LinearProgress
                        variant="determinate"
                        value={confidencePercent}
                        color={confidenceColor}
                        sx={{
                            height: 8,
                            borderRadius: 4,
                            backgroundColor: 'rgba(255,255,255,0.1)',
                            mb: 2,
                        }}
                    />

                    {result.confidence.reasoning && (
                        <Typography variant="body2" color="text.secondary">
                            {result.confidence.reasoning}
                        </Typography>
                    )}
                </Box>

                <Divider sx={{ mb: 3, borderColor: 'rgba(255,255,255,0.1)' }} />

                {/* AI Reasoning */}
                <Box>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                        <InfoIcon sx={{ mr: 1, color: 'secondary.main' }} />
                        <Typography variant="subtitle1" fontWeight={600}>
                            Detailed Reasoning
                        </Typography>
                    </Box>

                    <Box
                        sx={{
                            p: 2,
                            borderRadius: 2,
                            background: 'rgba(139, 92, 246, 0.1)',
                            border: '1px solid rgba(139, 92, 246, 0.2)',
                        }}
                    >
                        <Typography
                            variant="body2"
                            sx={{
                                lineHeight: 1.8,
                                whiteSpace: 'pre-wrap',
                            }}
                        >
                            {result.reasoning}
                        </Typography>
                    </Box>
                </Box>

                {/* Extracted Fields Summary */}
                {result.fields && (
                    <>
                        <Divider sx={{ my: 3, borderColor: 'rgba(255,255,255,0.1)' }} />

                        <Box>
                            <Typography variant="subtitle1" fontWeight={600} sx={{ mb: 2 }}>
                                Extracted Fields
                            </Typography>

                            <Box
                                sx={{
                                    p: 2,
                                    borderRadius: 2,
                                    background: 'rgba(255,255,255,0.05)',
                                }}
                            >
                                <Box component="pre" sx={{
                                    m: 0,
                                    fontSize: 12,
                                    color: 'text.secondary',
                                    fontFamily: 'monospace',
                                    whiteSpace: 'pre-wrap',
                                }}>
                                    {JSON.stringify(result.fields, null, 2)}
                                </Box>
                            </Box>
                        </Box>
                    </>
                )}
            </Box>
        </Drawer>
    );
}
