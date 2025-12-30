/**
 * Results Table Component
 * 
 * Displays validation results using MUI DataGrid with status chips
 */
'use client';

import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import { DataGrid, GridColDef, GridRenderCellParams } from '@mui/x-data-grid';
import FactCheckIcon from '@mui/icons-material/FactCheck';
import StatusChip from './StatusChip';
import { FieldValidation, ValidationStatus } from '@/types/validation';

interface ResultsTableProps {
    validations: FieldValidation[];
    onRowClick?: (field: string) => void;
}

const columns: GridColDef[] = [
    {
        field: 'field',
        headerName: 'Attribute',
        flex: 1,
        minWidth: 150,
        renderCell: (params: GridRenderCellParams) => (
            <Typography fontWeight={600} sx={{ textTransform: 'capitalize' }}>
                {params.value?.replace(/_/g, ' ')}
            </Typography>
        ),
    },
    {
        field: 'provided',
        headerName: 'Provided',
        flex: 1,
        minWidth: 120,
        renderCell: (params: GridRenderCellParams) => (
            <Typography color="text.secondary">
                {params.value || '—'}
            </Typography>
        ),
    },
    {
        field: 'expected',
        headerName: 'Expected',
        flex: 1,
        minWidth: 120,
        renderCell: (params: GridRenderCellParams) => (
            <Typography color="text.secondary">
                {params.value || '—'}
            </Typography>
        ),
    },
    {
        field: 'status',
        headerName: 'Status',
        width: 120,
        renderCell: (params: GridRenderCellParams<FieldValidation, ValidationStatus>) => (
            <StatusChip status={params.value!} size="small" />
        ),
    },
    {
        field: 'comment',
        headerName: 'Comment',
        flex: 2,
        minWidth: 200,
        renderCell: (params: GridRenderCellParams) => (
            <Typography
                sx={{
                    fontSize: 13,
                    lineHeight: 1.4,
                    whiteSpace: 'normal',
                    wordBreak: 'break-word',
                }}
            >
                {params.value}
            </Typography>
        ),
    },
];

export default function ResultsTable({ validations, onRowClick }: ResultsTableProps) {
    const rows = validations.map((v, index) => ({
        id: index,
        ...v,
    }));

    return (
        <Card sx={{ height: '100%' }}>
            <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                    <FactCheckIcon sx={{ fontSize: 32, mr: 1, color: 'primary.main' }} />
                    <Typography variant="h5" fontWeight={700}>
                        Validation Results
                    </Typography>
                </Box>

                {validations.length === 0 ? (
                    <Box
                        sx={{
                            height: 300,
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            flexDirection: 'column',
                            color: 'text.secondary',
                        }}
                    >
                        <FactCheckIcon sx={{ fontSize: 64, mb: 2, opacity: 0.3 }} />
                        <Typography>Submit a design to see validation results</Typography>
                    </Box>
                ) : (
                    <Box sx={{ width: '100%' }}>
                        <DataGrid
                            rows={rows}
                            columns={columns}
                            pageSizeOptions={[5, 10, 25]}
                            initialState={{
                                pagination: { paginationModel: { pageSize: 10 } },
                            }}
                            autoHeight
                            disableRowSelectionOnClick
                            onRowClick={(params) => onRowClick?.(params.row.field)}
                            sx={{
                                border: 'none',
                                '& .MuiDataGrid-cell': {
                                    borderColor: 'rgba(255,255,255,0.08)',
                                    py: 1.5,
                                },
                                '& .MuiDataGrid-columnHeaders': {
                                    background: 'rgba(59, 130, 246, 0.1)',
                                    borderRadius: '8px 8px 0 0',
                                },
                                '& .MuiDataGrid-row': {
                                    '&:hover': {
                                        background: 'rgba(59, 130, 246, 0.05)',
                                        cursor: 'pointer',
                                    },
                                },
                            }}
                            getRowHeight={() => 'auto'}
                        />
                    </Box>
                )}
            </CardContent>
        </Card>
    );
}
