import React, { useState, useRef, useEffect } from 'react';
import { ArrowUpRight, ArrowDownLeft, Clock, CheckCircle, XCircle, Filter } from 'lucide-react';
import { Transaction } from '../../types';
import { format } from 'date-fns';

interface TransactionHistoryProps {
  transactions: Transaction[];
}

const TransactionHistory: React.FC<TransactionHistoryProps> = ({ transactions: initialTransactions }) => {
  const [filter, setFilter] = useState<'all' | 'incoming_payment' | 'emi_blocked' | 'emi_paid'>('all');
  const [transactions, setTransactions] = useState<Transaction[]>(initialTransactions);
  
  useEffect(() => {
    setTransactions(initialTransactions); // Sync if prop changes
  }, [initialTransactions]);


  useEffect(() => {
      const socket = new WebSocket('ws://172.26.37.92/ws');
  
      socket.onopen = () => {
        console.log('WebSocket connected');
      };
  
      socket.onmessage = (event) => {
        try {
          const data: Transaction = JSON.parse(event.data);
  
          // Optional: basic validation
          if (data?.id && data?.type && data?.amount) {
            setTransactions(prev => [data, ...prev]);
          }
        } catch (error) {
          console.error('Invalid WebSocket message:', event.data);
        }
      };
  
      socket.onerror = (err) => {
        console.error('WebSocket error:', err);
      };
  
      socket.onclose = () => {
        console.log('WebSocket disconnected');
      };
  
      return () => {
        socket.close();
      };
    }, []);
  
  const filteredTransactions = filter === 'all' 
    ? transactions 
    : transactions.filter(t => t.type === filter);

  const getTransactionIcon = (type: Transaction['type']) => {
    switch (type) {
      case 'incoming_payment':
        return <ArrowDownLeft className="w-5 h-5 text-green-600" />;
      case 'emi_blocked':
        return <Clock className="w-5 h-5 text-orange-600" />;
      case 'emi_paid':
        return <ArrowUpRight className="w-5 h-5 text-blue-600" />;
      default:
        return <Clock className="w-5 h-5 text-gray-600" />;
    }
  };

  const getStatusIcon = (status: Transaction['status']) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-4 h-4 text-green-600" />;
      case 'pending':
        return <Clock className="w-4 h-4 text-orange-600" />;
      case 'failed':
        return <XCircle className="w-4 h-4 text-red-600" />;
    }
  };

  const getTypeLabel = (type: Transaction['type']) => {
    switch (type) {
      case 'incoming_payment':
        return 'Payment Received';
      case 'emi_blocked':
        return 'EMI Blocked';
      case 'emi_paid':
        return 'EMI Paid';
      case 'emi_scheduled':
        return 'EMI Scheduled';
      default:
        return type;
    }
  };

  const getAmountColor = (type: Transaction['type']) => {
    switch (type) {
      case 'incoming_payment':
        return 'text-green-600';
      case 'emi_blocked':
        return 'text-orange-600';
      case 'emi_paid':
        return 'text-blue-600';
      default:
        return 'text-gray-600';
    }
  };
    

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200">
      <div className="px-6 py-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-gray-900">Transaction History</h3>
          
          <div className="flex items-center space-x-2">
            <Filter className="w-4 h-4 text-gray-500" />
            <select
              value={filter}
              onChange={(e) => setFilter(e.target.value as any)}
              className="text-sm border border-gray-300 rounded-md px-3 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">All Transactions</option>
              <option value="incoming_payment">Payments Received</option>
              <option value="emi_blocked">EMI Blocked</option>
              <option value="emi_paid">EMI Paid</option>
            </select>
          </div>
        </div>
      </div>

      <div className="divide-y divide-gray-200 max-h-96 overflow-y-auto">
        {filteredTransactions.length === 0 ? (
          <div className="p-8 text-center text-gray-500">
            <Clock className="w-12 h-12 text-gray-300 mx-auto mb-4" />
            <p>No transactions found for the selected filter.</p>
          </div>
        ) : (
          filteredTransactions.map((transaction) => (
            <div key={transaction.id} className="p-6 hover:bg-gray-50 transition-colors">
              <div className="flex items-start justify-between">
                <div className="flex items-start space-x-4">
                  <div className="p-2 bg-gray-100 rounded-lg">
                    {getTransactionIcon(transaction.type)}
                  </div>
                  
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-1">
                      <h4 className="text-sm font-medium text-gray-900">
                        {getTypeLabel(transaction.type)}
                      </h4>
                      {getStatusIcon(transaction.status)}
                    </div>
                    
                    <p className="text-sm text-gray-600 mb-2">
                      {transaction.description}
                    </p>
                    
                    <p className="text-xs text-gray-500">
                      {format(new Date(transaction.timestamp), 'MMM dd, yyyy HH:mm')}
                    </p>
                    
                    {transaction.referenceNumber && (
                      <p className="text-xs text-gray-400 mt-1">
                        Ref: {transaction.referenceNumber}
                      </p>
                    )}
                  </div>
                </div>
                
                <div className="text-right">
                  <p className={`text-lg font-semibold ${getAmountColor(transaction.type)}`}>
                    {transaction.type === 'incoming_payment' ? '+' : '-'}₹{transaction.amount.toLocaleString()}
                  </p>
                  <span className={`inline-flex items-center text-xs font-medium px-2 py-1 rounded-full ${
                    transaction.status === 'completed' 
                      ? 'bg-green-100 text-green-800' 
                      : transaction.status === 'pending'
                      ? 'bg-orange-100 text-orange-800'
                      : 'bg-red-100 text-red-800'
                  }`}>
                    {transaction.status.charAt(0).toUpperCase() + transaction.status.slice(1)}
                  </span>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default TransactionHistory;