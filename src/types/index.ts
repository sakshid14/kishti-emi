export interface User {
  id: string;
  email: string;
  role: 'borrower' | 'lender';
  profile: BorrowerProfile | LenderProfile;
}

export interface BorrowerProfile {
  id: string;
  userId: string;
  businessName: string;
  ownerName: string;
  panNumber: string;
  gstNumber: string;
  businessAddress: string;
  contactNumber: string;
  bankAccountNumber: string;
  ifscCode: string;
  createdAt: string;
}

export interface LenderProfile {
  id: string;
  userId: string;
  organizationName: string;
  contactPerson: string;
  licenseNumber: string;
  address: string;
  contactNumber: string;
  email: string;
  createdAt: string;
}

export interface Loan {
  id: string;
  borrowerId: string;
  lenderId: string;
  lenderName: string;
  principalAmount: number;
  interestRate: number;
  tenureMonths: number;
  monthlyEmi: number;
  outstandingAmount: number;
  disbursementDate: string;
  emiDate: number; // Day of month (1-31)
  status: 'active' | 'closed' | 'defaulted';
  emiCollectionPercentage: number; // Percentage of incoming payments to block
}

export interface EMIWallet {
  id: string;
  borrowerId: string;
  currentBalance: number;
  totalMonthlyEmi: number;
  collectedThisMonth: number;
  lastUpdated: string;
}

export interface Transaction {
  id: string;
  borrowerId: string;
  loanId?: string;
  type: 'incoming_payment' | 'emi_blocked' | 'emi_paid' | 'emi_scheduled';
  amount: number;
  description: string;
  timestamp: string;
  status: 'completed' | 'pending' | 'failed';
  paymentMethod?: string;
  referenceNumber?: string;
}

export interface EMIPayment {
  id: string;
  loanId: string;
  borrowerId: string;
  lenderId: string;
  amount: number;
  dueDate: string;
  paidDate?: string;
  status: 'scheduled' | 'paid' | 'overdue' | 'failed';
}