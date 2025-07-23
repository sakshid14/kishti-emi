import React from 'react';
import { User, Wallet, AlertTriangle, CheckCircle } from 'lucide-react';
import { BorrowerProfile, EMIWallet, Loan } from '../../types';
import ProgressBar from '../common/ProgressBar';

interface BorrowerCardProps {
  borrower: BorrowerProfile;
  wallet: EMIWallet;
  loans: Loan[];
}

const BorrowerCard: React.FC<BorrowerCardProps> = ({ borrower, wallet, loans }) => {
  const totalLoanAmount = loans.reduce((sum, loan) => sum + loan.principalAmount, 0);
  const totalOutstanding = loans.reduce((sum, loan) => sum + loan.outstandingAmount, 0);
  const collectionPercentage = (wallet.collectedThisMonth / wallet.totalMonthlyEmi) * 100;
  
  const getStatusColor = () => {
    if (collectionPercentage >= 100) return 'text-green-600';
    if (collectionPercentage >= 75) return 'text-blue-600';
    return 'text-orange-600';
  };

  const getStatusIcon = () => {
    if (collectionPercentage >= 100) return <CheckCircle className="w-5 h-5 text-green-600" />;
    if (collectionPercentage >= 75) return <Wallet className="w-5 h-5 text-blue-600" />;
    return <AlertTriangle className="w-5 h-5 text-orange-600" />;
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-start space-x-4">
          <div className="p-3 bg-blue-50 rounded-lg">
            <User className="w-6 h-6 text-blue-600" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900">{borrower.businessName}</h3>
            <p className="text-sm text-gray-600">{borrower.ownerName}</p>
            <p className="text-xs text-gray-500">{loans.length} active loan{loans.length !== 1 ? 's' : ''}</p>
          </div>
        </div>
        
        <div className="flex items-center space-x-2">
          {getStatusIcon()}
          <span className={`text-sm font-medium ${getStatusColor()}`}>
            {collectionPercentage >= 100 ? 'Complete' : 
             collectionPercentage >= 75 ? 'On Track' : 'At Risk'}
          </span>
        </div>
      </div>

      <div className="space-y-4">
        {/* EMI Collection Progress */}
        <div>
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-gray-600">EMI Collection Progress</span>
            <span className="text-sm text-gray-500">This Month</span>
          </div>
          <ProgressBar
            value={wallet.collectedThisMonth}
            max={wallet.totalMonthlyEmi}
            color={collectionPercentage >= 100 ? 'green' : collectionPercentage >= 75 ? 'blue' : 'orange'}
          />
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-3 gap-4 pt-4 border-t border-gray-200">
          <div className="text-center">
            <p className="text-xs text-gray-500 mb-1">Wallet Balance</p>
            <p className="text-sm font-semibold text-gray-900">
              ₹{wallet.currentBalance.toLocaleString()}
            </p>
          </div>
          <div className="text-center">
            <p className="text-xs text-gray-500 mb-1">Monthly EMI</p>
            <p className="text-sm font-semibold text-gray-900">
              ₹{wallet.totalMonthlyEmi.toLocaleString()}
            </p>
          </div>
          <div className="text-center">
            <p className="text-xs text-gray-500 mb-1">Outstanding</p>
            <p className="text-sm font-semibold text-orange-600">
              ₹{totalOutstanding.toLocaleString()}
            </p>
          </div>
        </div>

        {/* Contact Information */}
        <div className="pt-4 border-t border-gray-200">
          <div className="flex justify-between text-sm">
            <span className="text-gray-600">Contact:</span>
            <span className="text-gray-900">{borrower.contactNumber}</span>
          </div>
          <div className="flex justify-between text-sm mt-1">
            <span className="text-gray-600">GST:</span>
            <span className="text-gray-900">{borrower.gstNumber}</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BorrowerCard;