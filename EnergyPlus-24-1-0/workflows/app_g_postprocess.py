# EnergyPlus, Copyright (c) 1996-2024, The Board of Trustees of the University
# of Illinois, The Regents of the University of California, through Lawrence
# Berkeley National Laboratory (subject to receipt of any required approvals
# from the U.S. Dept. of Energy), Oak Ridge National Laboratory, managed by UT-
# Battelle, Alliance for Sustainable Energy, LLC, and other contributors. All
# rights reserved.
#
# NOTICE: This Software was developed under funding from the U.S. Department of
# Energy and the U.S. Government consequently retains certain rights. As such,
# the U.S. Government has been granted for itself and others acting on its
# behalf a paid-up, nonexclusive, irrevocable, worldwide license in the
# Software to reproduce, distribute copies to the public, prepare derivative
# works, and perform publicly and display publicly, and to permit others to do
# so.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# (1) Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#
# (2) Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
# (3) Neither the name of the University of California, Lawrence Berkeley
#     National Laboratory, the University of Illinois, U.S. Dept. of Energy nor
#     the names of its contributors may be used to endorse or promote products
#     derived from this software without specific prior written permission.
#
# (4) Use of EnergyPlus(TM) Name. If Licensee (i) distributes the software in
#     stand-alone form without changes from the version obtained under this
#     License, or (ii) Licensee makes a reference solely to the software
#     portion of its product, Licensee must refer to the software as
#     "EnergyPlus version X" software, where "X" is the version number Licensee
#     obtained under this License and may not use a different name for the
#     software. Except as specifically required in this Section (4), Licensee
#     shall not use in a company name, a product name, in advertising,
#     publicity, or other promotional activities any name, trade name,
#     trademark, logo, or other designation of "EnergyPlus", "E+", "e+" or
#     confusingly similar designation, without the U.S. Department of Energy's
#     prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import os
import platform
import subprocess

from eplaunch.workflows.base import BaseEPLaunchWorkflow1, EPLaunchWorkflowResponse1


class AppGPostProcessWorkflow(BaseEPLaunchWorkflow1):

    def name(self):
        return "AppGPostProcess-24.1.0"

    def context(self):
        return "EnergyPlus-24.1.0-9d7789a3ac"

    def description(self):
        return "Run Appendix G Post Processor"

    def get_file_types(self):
        return ["*.html"]

    def get_output_suffixes(self):
        return ["-GAVG.html", "-GAVGMeter.csv", "-GAVGTable.txt"]

    def get_extra_data(self):
        return {"Hey, it's extra": "data"}

    def get_interface_columns(self):
        return []

    def main(self, run_directory, file_name, args):
        if 'workflow location' in args:
            energyplus_root_folder, _ = os.path.split(args['workflow location'])
            postprocess_folder = os.path.join(energyplus_root_folder, 'PostProcess')
            appgpp_folder = os.path.join(postprocess_folder, 'AppGPostProcess')
            if platform.system() == 'Windows':
                appgpp_binary = os.path.join(appgpp_folder, 'appgpostprocess.exe')
            else:
                appgpp_binary = os.path.join(appgpp_folder, 'appgpostprocess')
            if not os.path.exists(appgpp_binary):
                return EPLaunchWorkflowResponse1(
                    success=False,
                    message="AppGPostProcess binary not found: {}!".format(appgpp_binary),
                    column_data=[]
                )
        else:
            return EPLaunchWorkflowResponse1(
                success=False,
                message="Workflow location missing: {}!".format(args['worflow location']),
                column_data=[]
            )

        html_in_file_with_path = os.path.join(run_directory, file_name)
        html_in_file_no_ext, _ = os.path.splitext(html_in_file_with_path)
        if html_in_file_no_ext[-10:] != '-G000Table':
            return EPLaunchWorkflowResponse1(
                success=False,
                message='A file ending in -G000Table.html must be selected',
                column_data=[]
            )
        # else:
        # out_file_root = html_in_file_no_ext[:-10] + '-GAVG'
        # html_out_file = out_file_root + 'Table.html'
        # csv_out_file = out_file_root + '.csv'
        # csvmeter_out_file = out_file_root + 'Meter.csv'

        # copy input data file to working directory
        if os.path.exists(html_in_file_with_path) and os.path.exists(appgpp_binary) and os.path.exists(run_directory):

            # execute utility
            command_line_args = [appgpp_binary, html_in_file_with_path]
            process = subprocess.run(
                command_line_args,
                creationflags=subprocess.CREATE_NEW_CONSOLE,
                cwd=run_directory
            )
            if process.returncode == 0:
                return EPLaunchWorkflowResponse1(
                    success=True,
                    message="Ran AppendixGPostProcess OK for file: {}!".format(html_in_file_with_path),
                    column_data=[]
                )
            else:
                return EPLaunchWorkflowResponse1(
                    success=False,
                    message="AppendixGPostProcess failed for file: {}!".format(html_in_file_with_path),
                    column_data=[]
                )
        else:
            return EPLaunchWorkflowResponse1(
                success=False,
                message="AppendixGPostProcess files not found",
                column_data=[]
            )
