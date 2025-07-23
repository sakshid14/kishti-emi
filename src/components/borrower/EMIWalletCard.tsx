import React from 'react';
import { Wallet, Calendar, TrendingUp } from 'lucide-react';
import { EMIWallet } from '../../types';
import ProgressBar from '../common/ProgressBar';
import { format } from 'date-fns';

interface EMIWalletCardProps {
  wallet: EMIWallet;
}

const EMIWalletCard: React.FC<EMIWalletCardProps> = ({ wallet }) => {
  const collectionPercentage = (wallet.collectedThisMonth / wallet.totalMonthlyEmi) * 100;
  
  return (
    <div className="bg-gradient-to-br from-blue-50 to-indigo-100 rounded-xl shadow-lg border border-blue-200 p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-3">
          <div className="p-3 bg-blue-600 rounded-lg">
            <Wallet className="w-6 h-6 text-white" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900">EMI Wallet</h3>
            <p className="text-sm text-gray-600">
              Last updated: {format(new Date(wallet.lastUpdated), 'MMM dd, yyyy HH:mm')}
            </p>
          </div>
        </div>
      </div>

      <div className="space-y-4">
        <div className="bg-white rounded-lg p-4 shadow-sm">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-600">Current Balance</span>
            <TrendingUp className="w-4 h-4 text-green-600" />
          </div>
          <p className="text-3xl font-bold text-green-600">
            ₹{wallet.currentBalance.toLocaleString()}
          </p>
        </div>

        <div className="bg-white rounded-lg p-4 shadow-sm">
          <div className="flex items-center justify-between mb-3">
            <span className="text-sm font-medium text-gray-600">This Month's Collection</span>
            <Calendar className="w-4 h-4 text-blue-600" />
          </div>
          
          <ProgressBar
            value={wallet.collectedThisMonth}
            max={wallet.totalMonthlyEmi}
            color={collectionPercentage >= 100 ? 'green' : collectionPercentage >= 75 ? 'blue' : 'orange'}
          />
          
          <div className="mt-3 flex justify-between text-sm">
            <span className="text-gray-600">
              {collectionPercentage >= 100 ? 'Fully Collected' : 
               collectionPercentage >= 75 ? 'On Track' : 'Needs Attention'}
            </span>
            <span className={`font-medium ${
              collectionPercentage >= 100 ? 'text-green-600' : 
              collectionPercentage >= 75 ? 'text-blue-600' : 'text-orange-600'
            }`}>
              {collectionPercentage.toFixed(1)}%
            </span>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-3">
          <div className="bg-white rounded-lg p-3 shadow-sm text-center">
            <p className="text-xs text-gray-500 mb-1">Monthly EMI</p>
            <p className="text-lg font-bold text-gray-900">
              ₹{wallet.totalMonthlyEmi.toLocaleString()}
            </p>
          </div>
          <div className="bg-white rounded-lg p-3 shadow-sm text-center">
            <p className="text-xs text-gray-500 mb-1">Remaining</p>
            <p className="text-lg font-bold text-orange-600">
              ₹{(wallet.totalMonthlyEmi - wallet.collectedThisMonth).toLocaleString()}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EMIWalletCard;