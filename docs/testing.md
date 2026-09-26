# StockSense Testing Strategy

## Test Levels
1. **Unit & Invariant Tests (pytest):**
   - Invariant calculations (Receipt addition, Delivery deduction, Transfer preservation, Adjustment formula).
   - Password hashing and OTP generation/expiration verification.
2. **API & Integration Tests (pytest + httpx / TestClient):**
   - Auth endpoints (Register, Login, Protected routes, Password reset).
   - Master data CRUD (Products, Categories, Warehouses, Locations, Suppliers, Customers).
   - Inventory Operations workflow (Create Receipt -> Validate, Delivery Pick/Pack/Validate, Transfer Validate, Adjustment Validate).
   - Ledger integrity and pagination/filtering.
3. **Frontend Verification:**
   - TypeScript compiler verification (`tsc --noEmit`).
   - Vite production build verification (`npm run build`).
4. **End-to-End Demo Flow Test:**
   - Automated integration script executing the complete hackathon judging flow sequentially.
