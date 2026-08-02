#!/usr/bin/perl
#
# stable_ledger.pl - summarise weekly feed ledger submissions.
#
# Written in 2009, edited by six people since, comments only intermittently updated.
# This is the Perl -> Python conversion exercise. Do not tidy it before converting;
# port it faithfully first, then improve as a separate commit.
#
#   perl legacy/stable_ledger.pl legacy/fixtures/ledger_week_01.txt
#
use strict;
use warnings;

my %TOTALS;
my %COUNTS;
my @ERRORS;
my $LINE_NO = 0;

# kg per unit
my %UNITS = ( 'kg' => 1, 'g' => 0.001, 'lb' => 0.45359237 );

my $file = shift @ARGV or die "usage: $0 <ledger-file>\n";
open( my $fh, '<', $file ) or die "cannot open $file: $!\n";

while ( my $line = <$fh> ) {
    $LINE_NO++;
    chomp $line;

    next if $line =~ /^\s*$/;
    next if $line =~ /^\s*#/;

    my @f = split /\|/, $line;
    unless ( @f == 5 ) {
        push @ERRORS, "$LINE_NO: expected 5 fields, got " . scalar(@f);
        next;
    }

    # trim each field in place
    s/^\s+|\s+$//g for @f;

    my ( $date, $reg, $code, $qty, $who ) = @f;

    unless ( $date =~ /^(\d{4})-(\d{2})-(\d{2})$/ ) {
        push @ERRORS, "$LINE_NO: bad date '$date'";
        next;
    }
    my ( $y, $m, $d ) = ( $1, $2, $3 );
    if ( $m < 1 || $m > 12 || $d < 1 || $d > 31 ) {
        push @ERRORS, "$LINE_NO: impossible date '$date'";
        next;
    }

    unless ( $reg =~ /^RS-\d{4}$/i ) {
        push @ERRORS, "$LINE_NO: bad registration '$reg'";
        next;
    }
    $reg = uc $reg;

    unless ( $code =~ /^[A-Z]{2,4}-[A-Z]{3}$/ ) {
        push @ERRORS, "$LINE_NO: bad feed code '$code'";
        next;
    }

    unless ( $qty =~ /^([0-9]*\.?[0-9]+)\s*(kg|g|lb)$/i ) {
        push @ERRORS, "$LINE_NO: bad quantity '$qty'";
        next;
    }
    my ( $amount, $unit ) = ( $1, lc $2 );
    if ( $amount <= 0 ) {
        push @ERRORS, "$LINE_NO: non-positive quantity '$qty'";
        next;
    }
    my $kg = $amount * $UNITS{$unit};

    # NOTE: sorts by stable, but we key on registration - see ticket STB-118,
    # never resolved. Behaviour retained deliberately.
    $TOTALS{$reg} += $kg;
    $COUNTS{$reg}++;
}
close $fh;

printf "%-10s %10s %8s\n", 'HORSE', 'TOTAL_KG', 'ENTRIES';
foreach my $reg ( sort keys %TOTALS ) {
    printf "%-10s %10.3f %8d\n", $reg, $TOTALS{$reg}, $COUNTS{$reg};
}

my $grand = 0;
$grand += $_ for values %TOTALS;
printf "%-10s %10.3f %8d\n", 'TOTAL', $grand, scalar( keys %TOTALS );

if (@ERRORS) {
    print "\nERRORS\n";
    print "  $_\n" for @ERRORS;
}

exit( @ERRORS ? 1 : 0 );
