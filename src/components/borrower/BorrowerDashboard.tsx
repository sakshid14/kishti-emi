import React, {useEffect} from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { mockLoans, mockEMIWallets, mockTransactions } from '../../data/mockData';
import EMIWalletCard from './EMIWalletCard';
import LoansOverview from './LoansOverview';
import TransactionHistory from './TransactionHistory';
import StatsCard from '../common/StatsCard';
import { Wallet, CreditCard, TrendingUp, Calendar } from 'lucide-react';
import { BorrowerProfile } from '../../types';

const BorrowerDashboard: React.FC = () => {
  const { user } = useAuth();
  const userLoans = user.loans;
  const userWallet = user.emiWallet;
  const userTransactions = user.transactions;

  const totalLoanAmount = userLoans.reduce((sum, loan) => sum + loan.principalAmount, 0);
  const totalOutstanding = userLoans.reduce((sum, loan) => sum + loan.outstandingAmount, 0);
  const totalPaid = totalLoanAmount - totalOutstanding;
  const paymentCompletionRate = totalLoanAmount > 0 ? (totalPaid / totalLoanAmount) * 100 : 0;

  // Recent transactions (last 5)
  const recentTransactions = userTransactions
    .sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime())
    .slice(0, 10);

    useEffect(() => {
      console.log('user', user)
    }, [user])
    
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Welcome back {(user?.profile as BorrowerProfile).ownerName}!</h1>
        <p className="text-gray-600">
          Here's an overview of your EMI wallet and loan portfolio.
        </p>
      </div>

      {/* Top Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatsCard
          title="Active Loans"
          value={userLoans.length.toString()}
          subtitle="Total active loan accounts"
          icon={CreditCard}
          color="blue"
        />
        
        <StatsCard
          title="Current Wallet Balance"
          value={`₹${userWallet?.currentBalance.toLocaleString() || '0'}`}
          subtitle="Available for EMI payments"
          icon={Wallet}
          color="green"
        />
        
        <StatsCard
          title="Monthly EMI"
          value={`₹${userWallet?.totalMonthlyEmi.toLocaleString() || '0'}`}
          subtitle="Total across all loans"
          icon={Calendar}
          color="orange"
        />
        
        <StatsCard
          title="Payment Progress"
          value={`${paymentCompletionRate.toFixed(1)}%`}
          subtitle="Of total loan amount paid"
          icon={TrendingUp}
          color="purple"
          trend={{
            value: `₹${totalPaid.toLocaleString()} paid`,
            positive: true
          }}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* EMI Wallet - Takes more space */}
        <div className="lg:col-span-1">
          {userWallet ? (
            <EMIWalletCard wallet={userWallet} />
          ) : (
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <p className="text-gray-500">No EMI wallet found</p>
            </div>
          )}
        </div>

        {/* Recent Activity */}
        <div className="lg:col-span-2">
          <TransactionHistory transactions={recentTransactions} />
        </div>
      </div>

      {/* Loans Overview */}
      <div className="mt-8">
        <LoansOverview loans={userLoans} />
      </div>
    </div>
  );
};

export default BorrowerDashboard;