# CropYield Pro - AI Farming Advisor

## Overview

CropYield Pro is an AI-powered agricultural advisory system that provides farmers with crop yield predictions, profit estimates, personalized farming advice, and intelligent market price comparison. The application combines agricultural data analysis with AI-generated recommendations and agentic price comparison across multiple market platforms to help farmers make informed decisions about their crops and maximize profits. Users can input farming parameters such as crop type, location, investment amount, and farm size to receive comprehensive farming insights including yield forecasts, profitability analysis, market price analysis, selling strategy recommendations, and expert agricultural guidance.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web application with sidebar-based input forms
- **Layout**: Wide layout configuration with organized input sections for farming parameters
- **User Interface**: Form-based interface accepting crop selection, location, investment cost, and farm size inputs
- **Supported Crops**: Comprehensive selection including Rice, Wheat, Corn, Barley, Soybeans, Cotton, Sugarcane, and various vegetables and cash crops

### Backend Architecture
- **Modular Design**: Utility-based architecture with separate modules for different functionalities
- **Core Modules**:
  - `crop_data.py`: Handles yield estimation and profit calculations using agricultural base data with realistic quintal-based calculations
  - `openrouter_client.py`: Manages AI-powered farming advice generation through OpenRouter API
  - `price_comparison_agent.py`: Agentic AI system for intelligent market price comparison and selling strategy optimization
  - `crop_suitability.py`: Real-world crop-region compatibility checker with agricultural zone validation
- **Data Processing**: Mathematical models for yield prediction based on crop type, farm size, and regional factors
- **Agentic AI Features**: Autonomous price comparison across multiple market platforms with strategic selling recommendations

### Yield Prediction System
- **Base Yield Database**: Predefined yield data for 16 different crop types with variance factors
- **Regional Optimization**: Location-based multipliers for different Indian states and regions
- **Calculation Logic**: Combines base yields, farm size, regional factors, and realistic variance to generate estimates
- **Output Format**: Structured yield predictions with appropriate units (tons/kg) for different crops

### Profit Analysis Engine
- **Investment Tracking**: Processes total farming investment including seeds, fertilizers, and labor costs
- **ROI Calculation**: Generates return on investment percentages based on yield estimates and market prices
- **Risk Assessment**: Identifies and presents potential farming risks and mitigation strategies

### AI Advisory System
- **Integration**: OpenRouter API integration for AI-powered farming recommendations
- **Context Building**: Constructs comprehensive farmer profiles including crop, location, investment, and experience data
- **Structured Output**: JSON-formatted responses with growing tips, profit optimization, weather considerations, and best practices

### Agentic Price Comparison System
- **Market Intelligence**: Autonomous AI agent that analyzes crop prices across multiple market platforms and sources
- **Strategic Analysis**: AI-powered selling strategy recommendations based on net profit calculations, transport costs, and market conditions
- **Revenue Optimization**: Calculates maximum revenue potential by comparing wholesale markets, local mandis, export hubs, processing units, and direct consumer sales
- **Risk Assessment**: Identifies market-specific risks and provides timing advice for optimal selling decisions
- **Real-time Analytics**: Simulates market trend analysis and seasonal pricing patterns for informed decision-making

### Crop Suitability Intelligence
- **Regional Compatibility**: Real-world validation system that prevents cultivation of unsuitable crops based on soil type, climate, and agricultural zones
- **Alternative Recommendations**: Intelligent suggestion system that recommends suitable crops when selected crop cannot be grown in the specified region
- **Agricultural Science Integration**: Based on actual agricultural department data and regional crop patterns across Indian states
- **Smart Warnings**: Prevents unrealistic scenarios like rice cultivation in Rajasthan desert or sugarcane in cold mountain regions
- **Regional Optimization**: Suggests best crops for each region based on soil conditions, climate, and historical agricultural success

## External Dependencies

### AI Services
- **OpenRouter API**: Third-party AI service for generating personalized farming advice and recommendations
- **Authentication**: Requires OPENROUTER_API_KEY environment variable for API access

### Web Framework
- **Streamlit**: Python web application framework for creating the user interface and handling user interactions
- **OpenAI Python Client**: Used to interface with OpenRouter API endpoints

### Development Platform
- **Replit**: Cloud-based development and hosting environment for running the application
- **Environment Variables**: Secure API key management through environment configuration

### Regional Data Sources
- **Agricultural Database**: Built-in yield data covering major Indian agricultural regions including Punjab, Haryana, Maharashtra, Karnataka, and other farming states
- **Market Data**: Integrated pricing and profitability models for crop-specific revenue calculations