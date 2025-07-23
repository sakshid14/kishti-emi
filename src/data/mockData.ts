import { User, Loan, EMIWallet, Transaction, EMIPayment, BorrowerProfile, LenderProfile } from '../types';

export const mockUsers: User[] = [
  {
    id: '1',
    email: 'rajesh@techsolutions.com',
    role: 'borrower',
    profile: {
      id: '1',
      userId: '1',
      businessName: 'Tech Solutions Pvt Ltd',
      ownerName: 'Rajesh Kumar',
      panNumber: 'ABCDE1234F',
      gstNumber: '27ABCDE1234F1Z5',
      businessAddress: '123 Tech Park, Bangalore, Karnataka 560001',
      contactNumber: '+91-9876543210',
      bankAccountNumber: '1234567890',
      ifscCode: 'HDFC0001234',
      createdAt: '2024-01-15T00:00:00Z'
    } as BorrowerProfile
  },
  {
    id: '2',
    email: 'priya@manufacturing.com',
    role: 'borrower',
    profile: {
      id: '2',
      userId: '2',
      businessName: 'Priya Manufacturing',
      ownerName: 'Priya Sharma',
      panNumber: 'FGHIJ5678K',
      gstNumber: '19FGHIJ5678K2M9',
      businessAddress: '456 Industrial Area, Pune, Maharashtra 411001',
      contactNumber: '+91-9876543211',
      bankAccountNumber: '0987654321',
      ifscCode: 'ICICI0005678',
      createdAt: '2024-02-01T00:00:00Z'
    } as BorrowerProfile
  },
  {
    id: '3',
    email: 'contact@quickfinance.com',
    role: 'lender',
    profile: {
      id: '3',
      userId: '3',
      organizationName: 'Quick Finance Ltd',
      contactPerson: 'Amit Verma',
      licenseNumber: 'NBFC-2024-001',
      address: '789 Financial District, Mumbai, Maharashtra 400001',
      contactNumber: '+91-9876543212',
      email: 'contact@quickfinance.com',
      createdAt: '2024-01-01T00:00:00Z'
    } as LenderProfile
  }
];

export const mockLoans: Loan[] = [
  {
    id: '1',
    borrowerId: '1',
    lenderId: '3',
    lenderName: 'Quick Finance Ltd',
    principalAmount: 500000,
    interestRate: 12,
    tenureMonths: 24,
    monthlyEmi: 23539,
    outstandingAmount: 376312,
    disbursementDate: '2024-01-15T00:00:00Z',
    emiDate: 15,
    status: 'active',
    emiCollectionPercentage: 25
  },
  {
    id: '2',
    borrowerId: '1',
    lenderId: '3',
    lenderName: 'Quick Finance Ltd',
    principalAmount: 300000,
    interestRate: 10,
    tenureMonths: 36,
    monthlyEmi: 9676,
    outstandingAmount: 290000,
    disbursementDate: '2024-03-01T00:00:00Z',
    emiDate: 1,
    status: 'active',
    emiCollectionPercentage: 15
  },
  {
    id: '3',
    borrowerId: '2',
    lenderId: '3',
    lenderName: 'Quick Finance Ltd',
    principalAmount: 750000,
    interestRate: 14,
    tenureMonths: 18,
    monthlyEmi: 46875,
    outstandingAmount: 625000,
    disbursementDate: '2024-02-01T00:00:00Z',
    emiDate: 5,
    status: 'active',
    emiCollectionPercentage: 30
  }
];

export const mockEMIWallets: EMIWallet[] = [
  {
    id: '1',
    borrowerId: '1',
    currentBalance: 28500,
    totalMonthlyEmi: 33215,
    collectedThisMonth: 28500,
    lastUpdated: '2025-01-07T10:30:00Z'
  },
  {
    id: '2',
    borrowerId: '2',
    currentBalance: 35000,
    totalMonthlyEmi: 46875,
    collectedThisMonth: 35000,
    lastUpdated: '2025-01-07T14:20:00Z'
  }
];

export const mockTransactions: Transaction[] = [
  {
    id: '1',
    borrowerId: '1',
    loanId: '1',
    type: 'incoming_payment',
    amount: 50000,
    description: 'Payment received from client ABC Corp',
    timestamp: '2025-01-07T09:00:00Z',
    status: 'completed',
    paymentMethod: 'Bank Transfer',
    referenceNumber: 'TXN123456789'
  },
  {
    id: '2',
    borrowerId: '1',
    loanId: '1',
    type: 'emi_blocked',
    amount: 12500,
    description: 'EMI amount blocked (25% of ₹50,000)',
    timestamp: '2025-01-07T09:05:00Z',
    status: 'completed'
  },
  {
    id: '3',
    borrowerId: '1',
    loanId: '2',
    type: 'emi_blocked',
    amount: 7500,
    description: 'EMI amount blocked (15% of ₹50,000)',
    timestamp: '2025-01-07T09:05:00Z',
    status: 'completed'
  },
  {
    id: '4',
    borrowerId: '1',
    loanId: '1',
    type: 'emi_paid',
    amount: 23539,
    description: 'EMI payment to Quick Finance Ltd',
    timestamp: '2024-12-15T00:00:00Z',
    status: 'completed'
  }
];

export const mockEMIPayments: EMIPayment[] = [
  {
    id: '1',
    loanId: '1',
    borrowerId: '1',
    lenderId: '3',
    amount: 23539,
    dueDate: '2025-01-15T00:00:00Z',
    status: 'scheduled'
  },
  {
    id: '2',
    loanId: '2',
    borrowerId: '1',
    lenderId: '3',
    amount: 9676,
    dueDate: '2025-01-01T00:00:00Z',
    status: 'scheduled'
  },
  {
    id: '3',
    loanId: '3',
    borrowerId: '2',
    lenderId: '3',
    amount: 46875,
    dueDate: '2025-01-05T00:00:00Z',
    status: 'scheduled'
  }
];