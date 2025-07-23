import React, { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { mockUsers, mockLoans, mockEMIWallets, mockTransactions, mockEMIPayments } from '../../data/mockData';
import { BorrowerProfile } from '../../types';
import BorrowerCard from './BorrowerCard';
import StatsCard from '../common/StatsCard';
import { Users, DollarSign, TrendingUp, Calendar, Filter } from 'lucide-react';

const LenderDashboard: React.FC = () => {
  const { user } = useAuth();
  const [statusFilter, setStatusFilter] = useState<'all' | 'complete' | 'on_track' | 'at_risk'>('all');

  // Get lender's loans and borrowers
  const lenderLoans = mockLoans.filter(loan => loan.lenderId === user?.id);
  const lenderBorrowerIds = [...new Set(lenderLoans.map(loan => loan.borrowerId))];
  
  const borrowers = mockUsers
    .filter(u => u.role === 'borrower' && lenderBorrowerIds.includes(u.id))
    .map(u => u.profile as BorrowerProfile);

  // Calculate metrics
  const totalLoanAmount = lenderLoans.reduce((sum, loan) => sum + loan.principalAmount, 0);
  const totalOutstanding = lenderLoans.reduce((sum, loan) => sum + loan.outstandingAmount, 0);
  const totalMonthlyEmi = lenderLoans.reduce((sum, loan) => sum + loan.monthlyEmi, 0);
  
  // EMI collection status
  const borrowersWithWallets = borrowers.map(borrower => {
    const borrowerLoans = lenderLoans.filter(loan => loan.borrowerId === borrower.id);
    const wallet = mockEMIWallets.find(w => w.borrowerId === borrower.id);
    
    if (!wallet) return null;
    
    const collectionPercentage = (wallet.collectedThisMonth / wallet.totalMonthlyEmi) * 100;
    
    return {
      borrower,
      wallet,
      loans: borrowerLoans,
      status: collectionPercentage >= 100 ? 'complete' : 
              collectionPercentage >= 75 ? 'on_track' : 'at_risk'
    };
  }).filter(Boolean);

  // Filter borrowers based on status
  const filteredBorrowers = statusFilter === 'all' 
    ? borrowersWithWallets 
    : borrowersWithWallets.filter(b => b!.status === statusFilter);

  // Calculate status counts
  const statusCounts = {
    complete: borrowersWithWallets.filter(b => b!.status === 'complete').length,
    on_track: borrowersWithWallets.filter(b => b!.status === 'on_track').length,
    at_risk: borrowersWithWallets.filter(b => b!.status === 'at_risk').length,
  };

  // Expected EMI for this month
  const expectedEmiThisMonth = mockEMIPayments
    .filter(payment => payment.lenderId === user?.id && payment.status === 'scheduled')
    .reduce((sum, payment) => sum + payment.amount, 0);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Lender Dashboard</h1>
        <p className="text-gray-600">
          Monitor your borrowers' EMI collections and loan portfolio performance.
        </p>
      </div>

      {/* Top Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatsCard
          title="Total Borrowers"
          value={borrowers.length.toString()}
          subtitle="Active loan accounts"
          icon={Users}
          color="blue"
        />
        
        <StatsCard
          title="Loans Disbursed"
          value={`₹${totalLoanAmount.toLocaleString()}`}
          subtitle="Total principal amount"
          icon={DollarSign}
          color="green"
        />
        
        <StatsCard
          title="Outstanding Amount"
          value={`₹${totalOutstanding.toLocaleString()}`}
          subtitle="Remaining to be collected"
          icon={TrendingUp}
          color="orange"
        />
        
        <StatsCard
          title="Expected EMI"
          value={`₹${expectedEmiThisMonth.toLocaleString()}`}
          subtitle="This month's collection"
          icon={Calendar}
          color="purple"
        />
      </div>

      {/* Collection Status Summary */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">EMI Collection Status</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center p-4 bg-green-50 rounded-lg">
            <div className="text-2xl font-bold text-green-600 mb-1">{statusCounts.complete}</div>
            <div className="text-sm text-green-800">Fully Collected</div>
          </div>
          <div className="text-center p-4 bg-blue-50 rounded-lg">
            <div className="text-2xl font-bold text-blue-600 mb-1">{statusCounts.on_track}</div>
            <div className="text-sm text-blue-800">On Track (75%+)</div>
          </div>
          <div className="text-center p-4 bg-orange-50 rounded-lg">
            <div className="text-2xl font-bold text-orange-600 mb-1">{statusCounts.at_risk}</div>
            <div className="text-sm text-orange-800">At Risk (&lt;75%)</div>
          </div>
        </div>
      </div>

      {/* Borrower Cards */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <div className="px-6 py-4 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold text-gray-900">Borrower EMI Wallets</h3>
            
            <div className="flex items-center space-x-2">
              <Filter className="w-4 h-4 text-gray-500" />
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value as any)}
                className="text-sm border border-gray-300 rounded-md px-3 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="all">All Borrowers</option>
                <option value="complete">Fully Collected</option>
                <option value="on_track">On Track</option>
                <option value="at_risk">At Risk</option>
              </select>
            </div>
          </div>
        </div>

        <div className="p-6">
          {filteredBorrowers.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <Users className="w-12 h-12 text-gray-300 mx-auto mb-4" />
              <p>No borrowers found for the selected filter.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredBorrowers.map((item) => (
                <BorrowerCard
                  key={item!.borrower.id}
                  borrower={item!.borrower}
                  wallet={item!.wallet}
                  loans={item!.loans}
                />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default LenderDashboard;