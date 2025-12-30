/**
 * Status Chip Component
 * 
 * Color-coded chip for displaying PASS/WARN/FAIL validation status
 */
'use client';

import Chip from '@mui/material/Chip';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import WarningIcon from '@mui/icons-material/Warning';
import ErrorIcon from '@mui/icons-material/Error';
import { ValidationStatus } from '@/types/validation';

interface StatusChipProps {
    status: ValidationStatus;
    size?: 'small' | 'medium';
}

const statusConfig = {
    PASS: {
        color: 'success' as const,
        icon: <CheckCircleIcon />,
        label: 'PASS',
    },
    WARN: {
        color: 'warning' as const,
        icon: <WarningIcon />,
        label: 'WARN',
    },
    FAIL: {
        color: 'error' as const,
        icon: <ErrorIcon />,
        label: 'FAIL',
    },
};

export default function StatusChip({ status, size = 'medium' }: StatusChipProps) {
    const config = statusConfig[status];

    return (
        <Chip
            icon={config.icon}
            label={config.label}
            color={config.color}
            size={size}
            sx={{
                fontWeight: 700,
                minWidth: 90,
                '& .MuiChip-icon': {
                    fontSize: size === 'small' ? 16 : 20,
                },
            }}
        />
    );
}
