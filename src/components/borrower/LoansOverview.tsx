import React from 'react';
import { CreditCard, Building, Calendar, TrendingDown } from 'lucide-react';
import { Loan } from '../../types';
import { format } from 'date-fns';

interface LoansOverviewProps {
  loans: Loan[];
}

const LoansOverview: React.FC<LoansOverviewProps> = ({ loans }) => {
  const totalPrincipal = loans.reduce((sum, loan) => sum + loan.principalAmount, 0);
  const totalOutstanding = loans.reduce((sum, loan) => sum + loan.outstandingAmount, 0);
  const totalMonthlyEmi = loans.reduce((sum, loan) => sum + loan.monthlyEmi, 0);

  return (
    <div className="space-y-6">
      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Loan Amount</p>
              <p className="text-2xl font-bold text-gray-900">₹{totalPrincipal.toLocaleString()}</p>
            </div>
            <CreditCard className="w-8 h-8 text-blue-600" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Outstanding Amount</p>
              <p className="text-2xl font-bold text-orange-600">₹{totalOutstanding.toLocaleString()}</p>
            </div>
            <TrendingDown className="w-8 h-8 text-orange-600" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Monthly EMI</p>
              <p className="text-2xl font-bold text-green-600">₹{totalMonthlyEmi.toLocaleString()}</p>
            </div>
            <Calendar className="w-8 h-8 text-green-600" />
          </div>
        </div>
      </div>

      {/* Individual Loans */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Active Loans</h3>
        </div>
        
        <div className="divide-y divide-gray-200">
          {loans.map((loan) => (
            <div key={loan.id} className="p-6">
              <div className="flex items-start justify-between">
                <div className="flex items-start space-x-4">
                  <div className="p-3 bg-blue-50 rounded-lg">
                    <Building className="w-6 h-6 text-blue-600" />
                  </div>
                  <div>
                    <h4 className="text-lg font-medium text-gray-900">{loan.lenderName}</h4>
                    <p className="text-sm text-gray-600">
                      Disbursed: {format(new Date(loan.disbursementDate), 'MMM dd, yyyy')}
                    </p>
                    <div className="mt-2 flex items-center space-x-4 text-sm text-gray-600">
                      <span>Interest: {loan.interestRate}%</span>
                      <span>Tenure: {loan.tenureMonths} months</span>
                      <span>EMI Date: {loan.emiDate}th</span>
                    </div>
                  </div>
                </div>
                
                <div className="text-right">
                  <div className="space-y-2">
                    <div>
                      <p className="text-sm text-gray-600">Monthly EMI</p>
                      <p className="text-xl font-bold text-gray-900">₹{loan.monthlyEmi.toLocaleString()}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Outstanding</p>
                      <p className="text-lg font-semibold text-orange-600">₹{loan.outstandingAmount.toLocaleString()}</p>
                    </div>
                    <div className="bg-blue-50 px-3 py-1 rounded-full">
                      <p className="text-xs font-medium text-blue-800">
                        {loan.emiCollectionPercentage}% Auto-Collection
                      </p>
                    </div>
                  </div>
                </div>
              </div>
              
              {/* Progress Bar for Outstanding Amount */}
              <div className="mt-4">
                <div className="flex justify-between text-sm text-gray-600 mb-2">
                  <span>Loan Progress</span>
                  <span>{(((loan.principalAmount - loan.outstandingAmount) / loan.principalAmount) * 100).toFixed(1)}% paid</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-gradient-to-r from-green-500 to-green-600 h-2 rounded-full transition-all duration-300"
                    style={{
                      width: `${((loan.principalAmount - loan.outstandingAmount) / loan.principalAmount) * 100}%`
                    }}
                  />
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default LoansOverview;