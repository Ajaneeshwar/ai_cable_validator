/**
 * Input Panel Component
 * 
 * Handles both structured form input and free-text input for cable design validation
 */
'use client';

import { useState } from 'react';
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import Tab from '@mui/material/Tab';
import Tabs from '@mui/material/Tabs';
import MenuItem from '@mui/material/MenuItem';
import Select from '@mui/material/Select';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import CircularProgress from '@mui/material/CircularProgress';
import SendIcon from '@mui/icons-material/Send';
import ElectricalServicesIcon from '@mui/icons-material/ElectricalServices';
import { CableDesignInput, CableDesign } from '@/types/validation';

interface InputPanelProps {
    onValidate: (design?: CableDesignInput, freeText?: string, designId?: number) => void;
    isLoading: boolean;
    savedDesigns: CableDesign[];
}

interface TabPanelProps {
    children?: React.ReactNode;
    index: number;
    value: number;
}

function TabPanel({ children, value, index }: TabPanelProps) {
    return (
        <div hidden={value !== index} style={{ marginTop: 20 }}>
            {value === index && children}
        </div>
    );
}

const defaultDesign: CableDesignInput = {
    standard: 'IEC 60502-1',
    voltage: '0.6/1 kV',
    conductor_material: 'Cu',
    conductor_class: 'Class 2',
    csa: 10,
    insulation_material: 'PVC',
    insulation_thickness: 1.0,
};

export default function InputPanel({ onValidate, isLoading, savedDesigns }: InputPanelProps) {
    const [tabValue, setTabValue] = useState(0);
    const [design, setDesign] = useState<CableDesignInput>(defaultDesign);
    const [freeText, setFreeText] = useState('');
    const [selectedDesignId, setSelectedDesignId] = useState<number | ''>('');

    const handleTabChange = (_: React.SyntheticEvent, newValue: number) => {
        setTabValue(newValue);
    };

    const handleDesignChange = (field: keyof CableDesignInput, value: string | number) => {
        setDesign(prev => ({
            ...prev,
            [field]: value,
        }));
    };

    const handleSubmit = () => {
        if (tabValue === 0) {
            onValidate(design, undefined, undefined);
        } else if (tabValue === 1) {
            onValidate(undefined, freeText, undefined);
        } else if (tabValue === 2 && selectedDesignId !== '') {
            onValidate(undefined, undefined, selectedDesignId);
        }
    };

    const isValid = () => {
        if (tabValue === 0) return true;
        if (tabValue === 1) return freeText.trim().length > 0;
        if (tabValue === 2) return selectedDesignId !== '';
        return false;
    };

    return (
        <Card sx={{ height: '100%' }}>
            <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                    <ElectricalServicesIcon sx={{ fontSize: 32, mr: 1, color: 'primary.main' }} />
                    <Typography variant="h5" fontWeight={700}>
                        Cable Design Input
                    </Typography>
                </Box>

                <Tabs value={tabValue} onChange={handleTabChange} sx={{ mb: 2 }}>
                    <Tab label="Structured Input" />
                    <Tab label="Free Text" />
                    <Tab label="From Database" />
                </Tabs>

                <TabPanel value={tabValue} index={0}>
                    <Grid container spacing={2}>
                        <Grid item xs={12} sm={6}>
                            <FormControl fullWidth size="small">
                                <InputLabel>Standard</InputLabel>
                                <Select
                                    value={design.standard || ''}
                                    label="Standard"
                                    onChange={(e) => handleDesignChange('standard', e.target.value)}
                                >
                                    <MenuItem value="IEC 60502-1">IEC 60502-1</MenuItem>
                                    <MenuItem value="IEC 60502-2">IEC 60502-2</MenuItem>
                                </Select>
                            </FormControl>
                        </Grid>
                        <Grid item xs={12} sm={6}>
                            <FormControl fullWidth size="small">
                                <InputLabel>Voltage Rating</InputLabel>
                                <Select
                                    value={design.voltage || ''}
                                    label="Voltage Rating"
                                    onChange={(e) => handleDesignChange('voltage', e.target.value)}
                                >
                                    <MenuItem value="0.6/1 kV">0.6/1 kV</MenuItem>
                                    <MenuItem value="1.8/3 kV">1.8/3 kV</MenuItem>
                                </Select>
                            </FormControl>
                        </Grid>
                        <Grid item xs={12} sm={6}>
                            <FormControl fullWidth size="small">
                                <InputLabel>Conductor Material</InputLabel>
                                <Select
                                    value={design.conductor_material || ''}
                                    label="Conductor Material"
                                    onChange={(e) => handleDesignChange('conductor_material', e.target.value)}
                                >
                                    <MenuItem value="Cu">Copper (Cu)</MenuItem>
                                    <MenuItem value="Al">Aluminum (Al)</MenuItem>
                                </Select>
                            </FormControl>
                        </Grid>
                        <Grid item xs={12} sm={6}>
                            <FormControl fullWidth size="small">
                                <InputLabel>Conductor Class</InputLabel>
                                <Select
                                    value={design.conductor_class || ''}
                                    label="Conductor Class"
                                    onChange={(e) => handleDesignChange('conductor_class', e.target.value)}
                                >
                                    <MenuItem value="Class 1">Class 1 (Solid)</MenuItem>
                                    <MenuItem value="Class 2">Class 2 (Stranded)</MenuItem>
                                    <MenuItem value="Class 5">Class 5 (Flexible)</MenuItem>
                                    <MenuItem value="Class 6">Class 6 (Extra Flexible)</MenuItem>
                                </Select>
                            </FormControl>
                        </Grid>
                        <Grid item xs={12} sm={6}>
                            <TextField
                                fullWidth
                                size="small"
                                label="CSA (mm²)"
                                type="number"
                                value={design.csa || ''}
                                onChange={(e) => handleDesignChange('csa', parseFloat(e.target.value))}
                                inputProps={{ step: 0.5, min: 0.5 }}
                            />
                        </Grid>
                        <Grid item xs={12} sm={6}>
                            <FormControl fullWidth size="small">
                                <InputLabel>Insulation Material</InputLabel>
                                <Select
                                    value={design.insulation_material || ''}
                                    label="Insulation Material"
                                    onChange={(e) => handleDesignChange('insulation_material', e.target.value)}
                                >
                                    <MenuItem value="PVC">PVC</MenuItem>
                                    <MenuItem value="XLPE">XLPE</MenuItem>
                                    <MenuItem value="EPR">EPR</MenuItem>
                                </Select>
                            </FormControl>
                        </Grid>
                        <Grid item xs={12}>
                            <TextField
                                fullWidth
                                size="small"
                                label="Insulation Thickness (mm)"
                                type="number"
                                value={design.insulation_thickness || ''}
                                onChange={(e) => handleDesignChange('insulation_thickness', parseFloat(e.target.value))}
                                inputProps={{ step: 0.1, min: 0.1 }}
                            />
                        </Grid>
                    </Grid>
                </TabPanel>

                <TabPanel value={tabValue} index={1}>
                    <TextField
                        fullWidth
                        multiline
                        rows={4}
                        label="Cable Specification (Free Text)"
                        placeholder='Example: "IEC 60502-1 cable, 10 sqmm Cu Class 2, PVC insulation 1.0 mm, LV 0.6/1 kV"'
                        value={freeText}
                        onChange={(e) => setFreeText(e.target.value)}
                        sx={{ mb: 2 }}
                    />
                    <Typography variant="caption" color="text.secondary">
                        Enter a natural language description of the cable. The AI will extract and validate all parameters.
                    </Typography>
                </TabPanel>

                <TabPanel value={tabValue} index={2}>
                    <FormControl fullWidth size="small">
                        <InputLabel>Select Saved Design</InputLabel>
                        <Select
                            value={selectedDesignId}
                            label="Select Saved Design"
                            onChange={(e) => setSelectedDesignId(e.target.value as number)}
                        >
                            {savedDesigns.map((d) => (
                                <MenuItem key={d.id} value={d.id}>
                                    {d.name} ({d.csa} mm² {d.conductor_material})
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                    <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 2 }}>
                        Select a pre-saved cable design from the database to validate.
                    </Typography>
                </TabPanel>

                <Box sx={{ mt: 3 }}>
                    <Button
                        fullWidth
                        variant="contained"
                        size="large"
                        onClick={handleSubmit}
                        disabled={isLoading || !isValid()}
                        startIcon={isLoading ? <CircularProgress size={20} color="inherit" /> : <SendIcon />}
                        sx={{
                            py: 1.5,
                            background: 'linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)',
                            '&:hover': {
                                background: 'linear-gradient(135deg, #2563eb 0%, #7c3aed 100%)',
                            },
                        }}
                    >
                        {isLoading ? 'Validating...' : 'Validate Design'}
                    </Button>
                </Box>
            </CardContent>
        </Card>
    );
}
