from typing import List, Any, Optional
from mpyc.runtime import mpc
from mpyc.sectypes import SecFlt, SecInt
import numpy as np

class SecureComputation:
    def __init__(self):
        """Initialize secure computation environment"""
        self.mpc = mpc
        self.secflt = SecFlt()
        self.secint = SecInt()
        
    async def initialize(self):
        """Start MPC runtime with secure configuration"""
        await self.mpc.start()
        
    async def cleanup(self):
        """Cleanup MPC resources"""
        await self.mpc.shutdown()
        
    def secure_float(self, value: float) -> SecFlt:
        """Convert float to secure float"""
        return self.secflt(value)
        
    def secure_int(self, value: int) -> SecInt:
        """Convert int to secure int"""
        return self.secint(value)
        
    async def calculate_ema(self, prices: List[SecFlt], period: int) -> SecFlt:
        """Calculate EMA securely"""
        multiplier = self.secure_float(2 / (period + 1))
        
        @mpc.coroutine
        async def compute_ema():
            ema = prices[0]
            for price in prices[1:]:
                ema = price * multiplier + ema * (1 - multiplier)
            return ema
            
        return await compute_ema()
