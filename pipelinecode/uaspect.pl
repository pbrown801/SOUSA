#! /usr/bin/perl
######### 
#  needs a region file of this form
########## 
# Region file format: DS9 version 4.1
# Filename: SN2005cf_w1.img[UVW1]
#global color=green dashlist=8 3 width=1 font="helvetica 10 normal" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1
#fk5;circle(230.38417,-7.4132843,10.04")
#fk5;circle(230.37587,-7.4199785,10.04")
#fk5;circle(230.42453,-7.4353101,10.04")

#####################################################################################
# Calls XImage to do an interactive aspect correction for UVOT images.
#
# Stephen Holland,  2005-04-31, v0.1, First stab at the script
# Stephen Holland,  2005-04-01, v0.2, Automatically position and size image
# Stephen Holland,  2005-04-08, v0.3, Check that extension contains a 2D image
#####################################################################################

#use strict;
#use warnings;

use Astro::FITS::CFITSIO qw(:constants :longnames);

my $equinox = 2000.0;

die "usage: $0 fitsfile regionfile\n" if ( $#ARGV != 1 );

my $fitsfile   = $ARGV[0];
my $regionfile = $ARGV[1];

# Check the command line arguments.
die "error, $fitsfile does not exist, $!\n"   unless ( -e $fitsfile );
die "error, $regionfile does not exist, $!\n" unless ( -e $regionfile );

# Create the coordinates file
my $coofile = "AA_uaspect.coo";
unlink($coofile) || die "error, unable to unlink $coofile, $!\n" if ( -e $coofile );
open(COO,">$coofile") || die "error, unable to open $coofile for writing, $!\n";
open(REG,"<$regionfile") || die "error, unable to open $regionfile for reading, $!\n";
my @ra = ();
my @dec = ();
while ( <REG> ) {
    chomp;
    if ( m/^\S+;\S+\((\S+),(\S+),(\S+)\S*\)/ ) {
	print COO "$1 $2\n";
	push(@ra,$1);
	push(@dec,$2);
    }
}

# Estimate the size and position for displaying the image section
my $dra = 0.0;
my $ddec = 0.0;
for ( my $i = 0; $i <= $#ra; $i++ ) {
    for ( my $j = $i; $j <= $#ra; $j++ ) {
	my $delta1 = abs(  $ra[$j] -  $ra[$i] );
	my $delta2 = abs( $dec[$j] - $dec[$i] );
	$dra  = $delta1 if ( $delta1 > $dra  );
	$ddec = $delta2 if ( $delta2 > $ddec );
    }
}
my $size = ( $dra > $ddec ) ? -$dra*60.0 : -$ddec*60.0; # Convert to arcminutes
$size *= 2.0; # Double the size of the image to account for coordinate offsets
my $ra0 = 0.0;
foreach ( @ra ) {
    $ra0 += $_;
}

$ra0 /= ($#ra+1);
my $dec0 = 0.0;
foreach ( @dec ) {
    $dec0 += $_;
}
$dec0 /= ($#dec+1);
#print "dra,ddec = $dra,$ddec   size = $size   ra0,dec0 = $ra0,$dec0\n";

close(REG) || warn "warning, unable to close $regionfile, $!\n";
close(COO) || warn "warning, unable to close $coofile, $!\n";

# Get the number of HDUs in the FITS file.
my $fptr = undef;
my $status = 0;
&fits_open_file($fptr,$fitsfile,READWRITE(),$status);
die "error opening $fitsfile for reading, status = $status, $!\n" if ( $status != 0 );
my $hdunum = 0;
&fits_get_num_hdus($fptr,$hdunum,$status);
die "error getting number of HDUs in $fitsfile, status = $status, $!\n" if ( $status != 0 );
print "There are $hdunum HDUs in $fitsfile\n";

# Loop through the image extensions in the FITS file.
for ( my $i = 1; $i <= $hdunum; $i++ ) {

# Check that this HDU is an image.
    my $ihdu = $i - 1;
    my $image = $fitsfile."+".$ihdu;
    my $hdutype = 0;
    &fits_movabs_hdu($fptr,$i,$hdutype,$status);
    die "error getting HDU type from $image, status = $status, $!\n" if ( $status != 0 );
    my $comment = "";
    my $naxis = 0;
    &fits_read_key($fptr,TINT,'NAXIS',$naxis,$comment,$status);
    die "error reading NAXIS from $image, status = $status, $!\n" if ( $status != 0 );
    #print "$image has hdutype $hdutype and NAXIS=$naxis\n";
    next unless ( $hdutype == IMAGE_HDU()  &&  $naxis == 2 );
    print "Current image extension: $image\n";
# echo "we made it to the setup script"
# Set up the XImage script for cross-corrolation.
    my $script = "AA_uaspect.xco";
    unlink($script) || die "error, unable to unlink $script, $!\n" if ( -e $script );
    open(SCRIPT,">$script") || die "error, unable to open $script for writing, $!\n";
    print SCRIPT "read/size=$size/equinox=$equinox/ra=$ra0/dec=$dec0 $image\n";
    print SCRIPT "cpd /xtk\n";
    print SCRIPT "display/log\n";
    print SCRIPT "circle/regionfile=$regionfile/display\n";
    print SCRIPT "ccorr/norot/file=$coofile\n";
    print SCRIPT "exit\n";
    close(SCRIPT) || warn "warning, unable to close $script, $!\n";

# Run XImage to do the cross-corrolation
    my $output = "AA_uaspect.out";
    unlink($output) || die "error, unable to unlink $output, $!\n" if ( -e $output );
    my $command = "ximage \@$script > $output";
    system($command) && die "system call fails: $command, $!\n";

# Pull the new CRVAL values out of the ximage output.
    my $crval1 = 0;
    my $crval2 = 0;
    open(OUTPUT,"<$output") || die "error, unable to open $output for reading, $!\n";
    while ( <OUTPUT> ) {
	chomp;
	$crval1 = $1 if ( m/Map:\s*MAP1\s*Keyword:\s*CRVAL1\s*=\s*(\S+)/ );
	$crval2 = $1 if ( m/Map:\s*MAP1\s*Keyword:\s*CRVAL2\s*=\s*(\S+)/ );
    }
    close(OUTPUT) || warn "warning, unable to close $output, $!\n";
    print "$image     CRVAL1 = $crval1     CRVAL2 = $crval2\n";


# Update the CRVAL1 and CRVAL2 keywords in this HDU.
    &fits_modify_key_flt($fptr,'CRVAL1',$crval1,6,'&',$status);
    die "error modifying CRVAL1 in $image, status = $status, $!\n" if ( $status != 0 );
    &fits_modify_key_flt($fptr,'CRVAL2',$crval2,6,'&',$status);
    die "error modifying CRVAL2 in $image, status = $status, $!\n" if ( $status != 0 );

}

# Close the FITS file.
&fits_close_file($fptr,$status);
warn "warning unable to close $fitsfile, status = $status, $!\n" if ( $status != 0 );
