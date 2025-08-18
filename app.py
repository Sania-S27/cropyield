import streamlit as st
import os
from utils.openrouter_client import get_farming_advice
from utils.crop_data import get_yield_estimate, get_profit_estimate
from utils.price_comparison_agent import get_price_comparison_analysis
from utils.crop_suitability import check_crop_suitability, get_alternative_crops_for_region

# Page configuration
st.set_page_config(
    page_title="CropYield Pro - AI Farming Advisor",
    page_icon="🌾",
    layout="wide"
)

# Main title and description
st.title("🌾 CropYield Pro - AI Farming Advisor")
st.markdown("Get AI-powered farming advice, yield predictions, and profit estimates for your crops")

# Sidebar for inputs
with st.sidebar:
    st.header("📝 Farming Details")
    
    # Input fields
    seed_type = st.selectbox(
        "Seed Type",
        [
            "Rice", "Wheat", "Corn", "Barley", "Soybeans", "Cotton", 
            "Sugarcane", "Potato", "Tomato", "Onion", "Garlic", 
            "Chili", "Turmeric", "Ginger", "Tea", "Coffee"
        ],
        help="Select the type of crop you are planning to grow"
    )
    
    location = st.text_input(
        "Location (City, State/Region)",
        placeholder="e.g., Delhi, India",
        help="Enter your farming location for region-specific advice"
    )
    
    cost = st.number_input(
        "Total Investment (₹)",
        min_value=0,
        value=10000,
        step=1000,
        help="Enter your total farming investment including seeds, fertilizers, labor, etc."
    )
    
    farm_size = st.number_input(
        "Farm Size (acres)",
        min_value=0.1,
        value=1.0,
        step=0.1,
        help="Enter the size of your farm in acres"
    )
    
    farming_experience = st.selectbox(
        "Farming Experience",
        ["Beginner (0-2 years)", "Intermediate (3-10 years)", "Expert (10+ years)"],
        help="Your level of farming experience"
    )

# Main content area
if st.sidebar.button("🌱 Get AI Farming Advice", type="primary", use_container_width=True):
    if not seed_type or not location or cost <= 0:
        st.error("⚠️ Please fill in all required fields (seed type, location, and cost)")
    else:
        # First check crop suitability for the region
        suitability = check_crop_suitability(seed_type, location)
        
        if not suitability["suitable"]:
            # Show unsuitability warning
            st.error(f"🚫 {suitability['message']}")
            
            # Explain why it can't be grown
            st.warning(f"**Reason:** {suitability['reason']}")
            
            # Suggest alternative crops
            st.info("💡 **Recommended crops for your region:**")
            alternatives = suitability.get("alternatives", [])
            if alternatives:
                alternative_cols = st.columns(len(alternatives) if len(alternatives) <= 4 else 4)
                for i, alt_crop in enumerate(alternatives[:4]):
                    with alternative_cols[i]:
                        st.success(f"✅ {alt_crop}")
            
            # Show regional crop suggestions
            regional_crops = get_alternative_crops_for_region(location)
            st.markdown("### 🌾 Best Crops for Your Region:")
            crop_display_cols = st.columns(5)
            for i, crop in enumerate(regional_crops[:5]):
                with crop_display_cols[i]:
                    st.info(f"🌱 {crop}")
            
            # Stop further processing
            st.stop()
        
        else:
            # Show suitability confirmation
            st.success(f"✅ {suitability['message']}")
            if "optimal_conditions" in suitability:
                st.info(f"💡 {suitability['optimal_conditions']}")
    
        # Continue with original logic if crop is suitable
        # Create columns for layout
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            st.subheader("📊 Yield & Profit Estimates")
            
            # Show loading spinner
            with st.spinner("Calculating estimates..."):
                # Get yield and profit estimates
                yield_estimate = get_yield_estimate(seed_type, farm_size, location)
                profit_estimate = get_profit_estimate(seed_type, cost, yield_estimate, location)
            
            # Display estimates in metrics
            metric_col1, metric_col2 = st.columns(2)
            
            with metric_col1:
                st.metric(
                    label="Expected Yield",
                    value=f"{yield_estimate['amount']:.1f} {yield_estimate['unit']}",
                    delta=yield_estimate['confidence_note']
                )
            
            with metric_col2:
                st.metric(
                    label="Estimated Profit",
                    value=f"₹{profit_estimate['profit']:,.0f}",
                    delta=f"{profit_estimate['roi']:.1f}% ROI"
                )
            
            # Risk factors
            st.subheader("⚠️ Risk Factors")
            for risk in profit_estimate['risks']:
                st.warning(f"• {risk}")
        
        with col2:
            st.subheader("🤖 AI Farming Advice")
            
            # Get AI advice
            with st.spinner("Generating personalized farming advice..."):
                try:
                    advice = get_farming_advice(
                        seed_type=seed_type,
                        location=location,
                        cost=cost,
                        farm_size=farm_size,
                        experience=farming_experience,
                        yield_estimate=yield_estimate,
                        profit_estimate=profit_estimate
                    )
                    
                    if advice:
                        st.success("✅ AI Analysis Complete")
                        
                        # Display advice in expandable sections
                        with st.expander("🌱 Growing Tips", expanded=True):
                            st.write(advice.get('growing_tips', 'No specific tips available'))
                        
                        with st.expander("💰 Profit Optimization"):
                            st.write(advice.get('profit_tips', 'No specific profit tips available'))
                        
                        with st.expander("🌦️ Weather & Seasonal Advice"):
                            st.write(advice.get('weather_advice', 'No weather advice available'))
                        
                        with st.expander("🚜 Best Practices"):
                            st.write(advice.get('best_practices', 'No best practices available'))
                    
                except Exception as e:
                    st.error(f"❌ Failed to get AI advice: {str(e)}")
                    st.info("💡 This might be due to API connectivity issues. Please check your OpenRouter API key and try again.")
        
        with col3:
            st.subheader("💰 Smart Price Comparison")
            
            # Get price comparison analysis
            with st.spinner("Analyzing market prices across platforms..."):
                try:
                    price_analysis = get_price_comparison_analysis(
                        crop_type=seed_type,
                        location=location,
                        expected_yield=yield_estimate['amount'],
                        yield_unit=yield_estimate['unit']
                    )
                    
                    if price_analysis and 'error' not in price_analysis:
                        st.success("✅ Price Analysis Complete")
                        
                        # Show best market recommendation
                        if 'highest_net_price' in price_analysis:
                            best_market = price_analysis['highest_net_price']
                            st.metric(
                                label="Best Market Price",
                                value=f"₹{best_market['net_price']:.0f}/quintal",
                                delta=f"{best_market['market_name']}"
                            )
                        
                        # Revenue potential
                        if 'total_revenue_potential' in price_analysis:
                            revenue = price_analysis['total_revenue_potential']
                            st.metric(
                                label="Max Revenue Potential",
                                value=f"₹{revenue['best_market']:,.0f}",
                                delta=f"+₹{revenue['best_market'] - revenue['average_market']:,.0f} vs avg"
                            )
                        
                        # Market strategy
                        with st.expander("🎯 Selling Strategy", expanded=True):
                            if 'recommended_strategy' in price_analysis:
                                st.write(price_analysis['recommended_strategy'])
                        
                        with st.expander("📈 Market Analysis"):
                            if 'profit_analysis' in price_analysis:
                                st.write(price_analysis['profit_analysis'])
                        
                        with st.expander("⚠️ Market Risks"):
                            if 'risk_factors' in price_analysis:
                                risks = price_analysis['risk_factors']
                                if isinstance(risks, list):
                                    for risk in risks:
                                        st.warning(f"• {risk}")
                                else:
                                    st.write(risks)
                        
                        with st.expander("⏰ Timing Advice"):
                            if 'timing_advice' in price_analysis:
                                st.write(price_analysis['timing_advice'])
                        
                        # Price comparison table
                        with st.expander("📊 Market Price Comparison"):
                            if 'price_data' in price_analysis:
                                import pandas as pd
                                df = pd.DataFrame(price_analysis['price_data'])
                                df = df.sort_values('net_price', ascending=False)
                                st.dataframe(
                                    df[['market_name', 'price_per_quintal', 'transport_cost', 'net_price', 'distance']],
                                    use_container_width=True
                                )
                    else:
                        error_msg = price_analysis.get('error', 'Unknown error occurred')
                        st.error(f"❌ Price analysis failed: {error_msg}")
                        if 'basic_recommendation' in price_analysis:
                            st.info(f"💡 {price_analysis['basic_recommendation']}")
                        
                except Exception as e:
                    st.error(f"❌ Failed to get price analysis: {str(e)}")
                    st.info("💡 Price comparison temporarily unavailable. Check API connectivity.")
st.markdown("---")
st.subheader("ℹ️ About CropYield Pro")

info_col1, info_col2, info_col3 = st.columns(3)

with info_col1:
    st.markdown("""
    **🎯 Features:**
    - AI-powered farming advice
    - Yield predictions
    - Profit estimation
    - Smart price comparison
    - Market analysis & strategy
    - Risk assessment
    - Location-specific tips
    """)

with info_col2:
    st.markdown("""
    **🌾 Supported Crops:**
    - Cereals (Rice, Wheat, Corn)
    - Cash crops (Cotton, Sugarcane)
    - Vegetables (Potato, Tomato, Onion)
    - Spices (Turmeric, Chili, Ginger)
    - Plantation (Tea, Coffee)
    """)

with info_col3:
    st.markdown("""
    **📈 Benefits:**
    - Maximize crop yield
    - Optimize farming costs
    - Reduce farming risks
    - Get expert advice 24/7
    - Make data-driven decisions
    """)

# Footer
st.markdown("---")
st.markdown("*🤖 Powered by AI • Built for Indian Farmers • Version 1.0*")

# Check for API key
if not os.getenv("OPENROUTER_API_KEY"):
    st.warning("⚠️ OpenRouter API key not found. Please set the OPENROUTER_API_KEY environment variable to get AI farming advice.")
