import { Component } from 'react';

export default class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error, info) {
    // Log to console; could POST to backend if desired
    // eslint-disable-next-line no-console
    console.error('UI ErrorBoundary caught:', error, info);
  }

  handleRetry = () => {
    this.setState({ hasError: false });
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-[120px] m-4 p-4 rounded-2xl border border-amber-300 bg-amber-50 text-amber-800 shadow">
          <div className="font-semibold">Something went wrong.</div>
          <div className="text-sm opacity-80">Please try again.</div>
          <button onClick={this.handleRetry} className="mt-3 px-3 py-1.5 rounded-md bg-amber-600 text-white">Try Again</button>
        </div>
      );
    }
    return this.props.children;
  }
}
