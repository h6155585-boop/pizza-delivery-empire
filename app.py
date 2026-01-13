import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Page config for better width
st.set_page_config(page_title="Pizza Empire", layout="wide")

class PizzaDeliveryGame:
    def __init__(self, grid_size=10):
        self.grid_size = grid_size
        self.facility_cost = 2000
        self.delivery_cost_per_mile = 1
        
        # Initialize State
        if 'facilities' not in st.session_state:
            st.session_state.facilities = []
        if 'demand_map' not in st.session_state:
            # Create a fixed random seed for consistency or completely random
            st.session_state.demand_map = np.random.randint(10, 50, (grid_size, grid_size))

    def add_facility(self, x, y):
        # Check if location already exists to prevent duplicates
        if (x, y) in st.session_state.facilities:
            return False, "Facility already exists here!"
        
        if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
            st.session_state.facilities.append((x, y))
            return True, f"Facility added at ({x}, {y})"
        return False, "Coordinates out of bounds!"

    def calculate_costs(self):
        facilities = np.array(st.session_state.facilities)
        
        # If no facilities, cost is just 0 (or infinite strictly speaking, but 0 for game logic)
        if len(facilities) == 0:
            return 0, 0

        # Create coordinate grids
        X, Y = np.indices((self.grid_size, self.grid_size))
        
        # Vectorized Distance Calculation
        # This replaces the nested loops. We create a 3D array: (num_facilities, grid_x, grid_y)
        # We calculate distance from every grid point to every facility at once.
        distances = np.sqrt(
            (X[np.newaxis, :, :] - facilities[:, 0][:, np.newaxis, np.newaxis])**2 + 
            (Y[np.newaxis, :, :] - facilities[:, 1][:, np.newaxis, np.newaxis])**2
        )
        
        # Find minimum distance to any facility for every point on the grid
        min_distances = np.min(distances, axis=0)
        
        # Calculate Costs
        total_delivery_cost = np.sum(min_distances * st.session_state.demand_map * self.delivery_cost_per_mile)
        total_facility_cost = len(facilities) * self.facility_cost
        
        return total_facility_cost, total_delivery_cost
def find_best_two_facilities(self, target=10000):
    X, Y = np.indices((self.grid_size, self.grid_size))
    demand = st.session_state.demand_map

    best_pair = None
    best_diff = float("inf")
    best_cost = None

    for x1 in range(self.grid_size):
        for y1 in range(self.grid_size):
            for x2 in range(self.grid_size):
                for y2 in range(self.grid_size):
                    facilities = np.array([(x1, y1), (x2, y2)])

                    distances = np.sqrt(
                        (X[np.newaxis] - facilities[:, 0][:, None, None])**2 +
                        (Y[np.newaxis] - facilities[:, 1][:, None, None])**2
                    )

                    min_dist = np.min(distances, axis=0)
                    delivery_cost = np.sum(min_dist * demand)

                    total_cost = 2 * self.facility_cost + delivery_cost
                    diff = abs(total_cost - target)

                    if diff < best_diff:
                        best_diff = diff
                        best_pair = ((x1, y1), (x2, y2))
                        best_cost = total_cost

    return best_pair, best_cost

    def plot_network(self):
        # Create the Heatmap for Demand
        fig = px.imshow(
            st.session_state.demand_map,
            labels=dict(x="Y Coordinate", y="X Coordinate", color="Demand"),
            x=np.arange(self.grid_size),
            y=np.arange(self.grid_size),
            color_continuous_scale='YlOrRd',
            origin='lower' # Matches standard cartesian plot
        )

        # Overlay Facilities if they exist
        if st.session_state.facilities:
            facilities = np.array(st.session_state.facilities)
            # Note: In imshow with origin='lower', we map X to y-axis and Y to x-axis usually, 
            # but based on your original logic: row=x, col=y.
            
            fig.add_trace(go.Scatter(
                x=facilities[:, 1], # Column index (Y)
                y=facilities[:, 0], # Row index (X)
                mode='markers',
                marker=dict(symbol='triangle-up', size=15, color='blue', line=dict(width=2, color='white')),
                name='Facilities'
            ))

        fig.update_layout(
            margin=dict(l=0, r=0, t=30, b=0),
            height=500,
            xaxis=dict(tickmode='linear', dtick=1),
            yaxis=dict(tickmode='linear', dtick=1)
        )
        return fig

def main():
    st.title("🍕 Pizza Delivery Empire Game")
    
    # Initialize game
    game = PizzaDeliveryGame(grid_size=10)
    
    # Layout: Plot on Left (2/3), Controls on Right (1/3)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.plotly_chart(game.plot_network(), use_container_width=True)
    
    with col2:
        st.subheader("Operations")
        
        # 1. Add Facility Form (Prevents reload while typing)
        with st.form("add_facility_form"):
            st.write("**New Facility Location**")
            c1, c2 = st.columns(2)
            with c1:
                x_input = st.number_input("X (Row)", 0, game.grid_size-1, step=1)
            with c2:
                y_input = st.number_input("Y (Col)", 0, game.grid_size-1, step=1)
                
            submitted = st.form_submit_button("📍 Build Facility")
            
            if submitted:
                success, msg = game.add_facility(x_input, y_input)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

        # 2. Cost Analysis
        st.divider()
       if st.button("💰 Calculate Financials", type="primary", use_container_width=True):
    f_cost, d_cost = game.calculate_costs()
    t_cost = f_cost + d_cost

    st.metric("Total Costs", f"${t_cost:,.2f}")

    c1, c2 = st.columns(2)
    c1.caption(f"Facilities: ${f_cost:,.0f}")
    c2.caption(f"Delivery: ${d_cost:,.0f}")

st.divider()
if st.button("🎯 Auto-Find 2 Facilities (~$10K)", use_container_width=True):
    pair, cost = game.find_best_two_facilities()
    st.success(f"Facility 1: {pair[0]} | Facility 2: {pair[1]}")
    st.metric("Optimized Total Cost", f"${cost:,.2f}")

c1, c2 = st.columns(2)
            c1.caption(f"Facilities: ${f_cost:,.0f}")
            c2.caption(f"Delivery: ${d_cost:,.0f}")

        # 3. Reset
        st.divider()
        if st.button("🔄 Reset Simulation", use_container_width=True):
            st.session_state.facilities = []
            st.session_state.demand_map = np.random.randint(10, 50, (game.grid_size, game.grid_size))
            st.rerun()

if __name__ == "__main__":
    main()

Answer ??
