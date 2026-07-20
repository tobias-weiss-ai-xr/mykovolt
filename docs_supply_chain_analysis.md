# Supply Chain Analysis [TRL 2 — PROVISIONAL]

> **⚠️ This document is forward-looking.** MykoVolt is at TRL 2 (simulation phase, no prototype). Specific component pricing, lead times, and supplier details are preliminary estimates based on Open-Source Bill-of-Materials research. Actual supply chain validation begins at TRL 5+. All costs are in USD as preliminary estimates; final BoM pricing in EUR may differ.

## Executive Summary

This document outlines a preliminary component redundancy framework for the MykoVolt bio-battery project. It identifies critical electronic components for the Developer Kit board, establishes backup suppliers, and develops alternative architectures. This is a reference skeleton — the details will be validated during Phase 1 (Lab Validation → Prototype).

## Critical Components Identified

### Primary Components
1. **NFC Controller (ST25DV04K)** - Primary communication interface
2. **Microcontroller (STM32L011K4)** - Core processing unit
3. **Power Management IC (BQ25570)** - Energy regulation and optimization
4. **FRAM Memory (MB85RC16)** - Non-volatile data storage
5. **Capacitive Sensor (FDC1004)** - Soil moisture measurement

### Backup Components
1. **Alternative NFC**: NT3H2513, M24SR64
2. **Alternative MCU**: STM32L0522, NRF52832
3. **Alternative Power**: TPS63070, LM3607
4. **Alternative Memory**: MR46V1M, FM28V10
5. **Alternative Sensor**: HTS221, BME280

## Supply Chain Analysis

### Current Supplier Dependencies

| Component | Primary Supplier | Lead Time | Risk Level | Backup Options |
|-----------|------------------|-----------|------------|----------------|
| ST25DV04K | STMicroelectronics | 6-8 weeks | High | NT3H2513, M24SR64 |
| STM32L011K4 | STMicroelectronics | 4-6 weeks | Medium | STM32L0522, NRF52832 |
| BQ25570 | Texas Instruments | 3-4 weeks | Low | TPS63070, LM3607 |
| MB85RC16 | Fujitsu | 5-7 weeks | Medium | MR46V1M, FM28V10 |
| FDC1004 | ON Semiconductor | 4-5 weeks | High | HTS221, BME280 |

### Risk Assessment Matrix

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Supply disruption | Medium | High | Dual sourcing, inventory buffer |
| Price volatility | High | Medium | Alternative components, bulk purchasing |
| Technical obsolescence | Low | High | Regular component review, forward planning |
| Quality issues | Medium | Medium | Supplier qualification, quality audits |

## Alternative Architecture Design

### Primary Architecture
```
STM32L011K4 (MCU) → BQ25570 (Power) → ST25DV04K (NFC) → FDC1004 (Sensor) → MB85RC16 (FRAM)
```

### Alternative Architecture 1
```
STM32L0522 (MCU) → TPS63070 (Power) → NT3H2513 (NFC) → HTS221 (Sensor) → MR46V1M (FRAM)
```

### Alternative Architecture 2
```
NRF52832 (MCU) → LM3607 (Power) → M24SR64 (NFC) → BME280 (Sensor) → FM28V10 (FRAM)
```

## Cost Analysis

### Component Cost Comparison

| Component | Primary Cost | Backup Cost | Savings Potential |
|-----------|--------------|-------------|------------------|
| NFC Controller | $1.20 | $0.95 | 21% |
| Microcontroller | $1.50 | $2.10 | -40% |
| Power Management | $3.50 | $2.80 | 20% |
| FRAM Memory | $1.80 | $2.20 | -22% |
| Capacitive Sensor | $3.00 | $2.50 | 17% |

### Total Cost Impact
- **Primary Architecture**: $13.00 per unit
- **Alternative 1**: $12.95 per unit
- **2 Alternative 2**: $13.20 per unit

## Implementation Timeline

### Month 1: Component Research
- Research backup suppliers
- Evaluate technical specifications
- Cost analysis and budgeting
- Risk assessment

### Month 2: Supplier Qualification
- Contact potential backup suppliers
- Technical evaluation and testing
- Quality assurance verification
- Contract negotiation

### Month 3: Architecture Validation
- Build proof-of-concept with backup components
- Performance testing and validation
- Cost-benefit analysis
- Documentation and reporting

## Quality Assurance

### Supplier Qualification Process
1. **Technical Evaluation**: Component specifications and performance
2. **Financial Stability**: Credit rating and financial health
3. **Production Capacity**: Manufacturing capabilities and lead times
4. **Quality Systems**: ISO certification and quality control processes
5. **Logistics**: Shipping, customs, and distribution capabilities

### Quality Control Procedures
- **Incoming Inspection**: 100% testing of critical components
- **Process Validation**: Manufacturing process verification
- **Final Testing**: Complete system integration testing
- **Documentation**: Full traceability and documentation

## Risk Mitigation Strategies

### Supply Chain Diversification
- **Multiple Suppliers**: Establish relationships with 2-3 suppliers per component
- **Geographic Distribution**: Diversify supplier locations globally
- **Inventory Buffering**: Maintain safety stock for critical components
- **Rapid Requisition**: Streamlined procurement processes for emergencies

### Technical Risk Mitigation
- **Component Standardization**: Use standardized interfaces where possible
- **Modular Design**: Design for easy component replacement
- **Documentation**: Comprehensive component documentation and specifications
- **Training**: Staff training on component replacement procedures

### Financial Risk Mitigation
- **Cost Monitoring**: Regular cost reviews and analysis
- **Budget Contingency**: Allocate funds for emergency purchases
- **Price Lock**: Negotiate long-term pricing agreements where possible
- **Alternative Sourcing**: Identify and qualify alternative suppliers

## Conclusion

The component redundancy strategy provides a comprehensive approach to managing supply chain risks while maintaining cost efficiency and technical performance. By implementing this strategy, the MykoVolt project will be better positioned to handle supply disruptions, price volatility, and technical challenges.

Key Success Factors:
- Early supplier identification and qualification
- Continuous monitoring and evaluation
- Flexible procurement processes
- Comprehensive documentation and knowledge management
- Regular review and optimization of the redundancy strategy

This plan ensures project continuity while maintaining the high technical standards and quality expectations of the MykoVolt bio-battery system.